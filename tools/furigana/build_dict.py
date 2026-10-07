#!/usr/bin/env python3
"""ふりがな辞書の生成（ITパスポートのページ用）

ページの文章（テキストの塊）ごとに、文脈つきで漢字の読みを決めて、ページごとの辞書JSONを作る。
ブラウザ側（app.js）が、トグルをオンにしたときだけ辞書を読み込み、読みをルビとして表示する。

使い方（リポジトリのルートで）:
  tools/furigana/.venv/bin/python tools/furigana/build_dict.py            # 辞書を作る（body に data-furigana も付ける）
  tools/furigana/.venv/bin/python tools/furigana/build_dict.py --list     # 単語と読みの一覧（レビュー用）
  tools/furigana/.venv/bin/python tools/furigana/build_dict.py --check    # 辞書で覆えない漢字の数（0が目標）

誤読は overrides.tsv で直す（列: 表記 / ふりがなを付ける部分 / 読み）。
辞書の形式: {"v":1,"n":{"<FNV-1aハッシュ>.<UTF-16長>":[[開始,長さ,"よみ"],...]}}（位置は文章の塊の中、UTF-16単位）
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COURSE_DIR = ROOT / 'it-passport-technology'
DICT_DIR = COURSE_DIR / 'furigana'
OVERRIDES = Path(__file__).with_name('overrides.tsv')
DEFAULT_PAGES = ['it-passport-technology.html', 'it-passport-technology/week*.html']

KANJI_RE = re.compile(r'[㐀-䶿一-鿿々〆]')
EXCLUDE_TAGS = {'script', 'style', 'code', 'pre', 'textarea', 'title', 'noscript', 'svg', 'ruby', 'head'}
VOID_TAGS = {'br', 'wbr', 'img', 'input', 'meta', 'link', 'hr', 'source', 'area', 'col', 'embed', 'base', 'track'}
BLOCK_TAGS = {'p', 'li', 'ul', 'ol', 'td', 'th', 'tr', 'table', 'thead', 'tbody', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
              'div', 'section', 'header', 'footer', 'main', 'nav', 'summary', 'details', 'figure', 'figcaption',
              'dt', 'dd', 'dl', 'blockquote', 'body', 'html', 'button', 'label', 'option', 'select', 'form', 'br'}


def is_kanji(ch):
    return bool(KANJI_RE.match(ch))


def kata2hira(s):
    return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in s)


def node_key(text):
    """ノードの文字列のキー（FNV-1a 32bit、UTF-16の単位で計算。app.js の nodeKey と同じ）"""
    h = 0x811C9DC5
    b = text.encode('utf-16-le')
    for i in range(0, len(b), 2):
        h ^= b[i] | (b[i + 1] << 8)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return '%08x.%d' % (h, len(b) // 2)


def utf16_len(s):
    return len(s.encode('utf-16-le')) // 2


def utf16_pos(s, idx):
    """文字列の位置 idx（コードポイント）を UTF-16 の位置に直す"""
    return utf16_len(s[:idx])


# ---------------------------------------------------------------- HTML を「文章の塊」に分ける
class BlockCollector(HTMLParser):
    """本文のテキストノードを、ブロック単位（p/li/td…）にまとめて集める。除外要素の中は集めない。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []        # (tag, 除外か)
        self.excl = 0
        self.buf = ''          # 連続する handle_data を1つのテキストノードにまとめる
        self.nodes = []        # いまのブロックのテキストノード
        self.blocks = []       # 完了したブロック（テキストノードのリスト）
        self.all_nodes = []    # 除外外のすべてのテキストノード（被覆チェック用）

    def _end_node(self):
        if self.buf:
            self.nodes.append(self.buf)
            self.all_nodes.append(self.buf)
            self.buf = ''

    def _flush(self):
        self._end_node()
        if self.nodes:
            self.blocks.append(self.nodes)
            self.nodes = []

    def handle_starttag(self, tag, attrs):
        self._end_node()
        excluded = tag in EXCLUDE_TAGS or any(k == 'data-no-furigana' for k, _ in attrs)
        if tag in BLOCK_TAGS or excluded:
            self._flush()
        if tag in VOID_TAGS:
            return
        self.stack.append((tag, excluded))
        if excluded:
            self.excl += 1

    def handle_startendtag(self, tag, attrs):
        self._end_node()
        if tag in BLOCK_TAGS:
            self._flush()

    def handle_endtag(self, tag):
        self._end_node()
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                popped = self.stack[i:]
                del self.stack[i:]
                self.excl -= sum(1 for _, e in popped if e)
                if tag in BLOCK_TAGS or any(e for _, e in popped):
                    self._flush()
                return

    def handle_data(self, data):
        if self.excl > 0:
            return
        self.buf += data

    def close(self):
        super().close()
        self._flush()


def collect_blocks(html_text):
    p = BlockCollector()
    p.feed(html_text)
    p.close()
    return p.blocks, p.all_nodes


# ---------------------------------------------------------------- 読みの決定
def load_overrides(path=OVERRIDES):
    """overrides.tsv: 表記<TAB>ふりがなを付ける部分(-なら表記全体)<TAB>読み。長い表記を先に使う。"""
    rows = []
    if not path.exists():
        return rows
    for ln, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        cols = line.split('\t')
        if len(cols) != 3:
            raise ValueError('overrides.tsv %d行目: 3列（表記・付ける部分・読み）が必要です: %r' % (ln, line))
        surface, target, reading = cols[0].strip(), cols[1].strip(), cols[2].strip()
        if target == '-':
            target = surface
        if target not in surface:
            raise ValueError('overrides.tsv %d行目: 付ける部分が表記に含まれません: %r' % (ln, line))
        rows.append((surface, target, kata2hira(reading)))
    rows.sort(key=lambda r: -len(r[0]))
    return rows


def align(surface, reading):
    """表記（漢字＋送り仮名）と読みから、漢字の連続ごとの読みを返す。[(開始, 終了, 読み)]。できなければ None。
    例: 受け取る / うけとる -> [(0,1,'う'), (2,3,'と')]"""
    hira = kata2hira(reading)
    parts, i = [], 0
    while i < len(surface):
        kind = is_kanji(surface[i])
        j = i
        while j < len(surface) and is_kanji(surface[j]) == kind:
            j += 1
        parts.append((kind, i, j))
        i = j
    regex = ''.join('(.+?)' if k else re.escape(kata2hira(surface[a:b])) for k, a, b in parts)
    m = re.fullmatch(regex, hira)
    if not m:
        return None
    out, g = [], 1
    for k, a, b in parts:
        if k:
            out.append((a, b, m.group(g)))
            g += 1
    return out


MIN_BUN = {'1': 'ぷん', '2': 'ふん', '3': 'ぷん', '4': 'ぷん', '5': 'ふん', '6': 'ぷん', '7': 'ふん', '8': 'ぷん', '9': 'ふん', '0': 'ぷん'}
DAYS = {1: 'ついたち', 2: 'ふつか', 3: 'みっか', 4: 'よっか', 5: 'いつか', 6: 'むいか', 7: 'なのか', 8: 'ようか', 9: 'ここのか',
        10: 'とおか', 14: 'じゅうよっか', 20: 'はつか', 24: 'にじゅうよっか'}


def counter_assignments(text):
    """数字＋助数詞（分・月・日・人）の読みを規則で決める。[(開始, 終了, 読み)]（text上の位置）"""
    out = []
    for m in re.finditer(r'(\d+)分(?![野類析散割別担離子配布岐解数量])', text):
        out.append((m.end() - 1, m.end(), MIN_BUN[m.group(1)[-1]]))
    for m in re.finditer(r'(\d+)月(?:(\d+)日)?', text):
        gl = len(m.group(1))
        out.append((m.start() + gl, m.start() + gl + 1, 'がつ'))
        if m.group(2):
            n = int(m.group(2))
            if n in DAYS:
                out.append((m.start(2), m.end(), DAYS[n]))      # 日付: 数字ごと（7日=なのか）
            else:
                out.append((m.end() - 1, m.end(), 'にち'))
    for m in re.finditer(r'(?<![\d月])(\d+)日', text):
        n = int(m.group(1))
        if n in DAYS and n != 1:
            out.append((m.start(), m.end(), DAYS[n]))
        else:
            out.append((m.end() - 1, m.end(), 'にち'))
    for m in re.finditer(r'(\d+)人', text):
        n = m.group(1)
        if n == '1':
            out.append((m.start(), m.end(), 'ひとり'))
        elif n == '2':
            out.append((m.start(), m.end(), 'ふたり'))
        else:
            out.append((m.end() - 1, m.end(), 'にん'))
    return out


class Analyzer:
    def __init__(self, overrides=None):
        import fugashi
        self.tagger = fugashi.Tagger()
        self.overrides = overrides if overrides is not None else load_overrides()
        self.missing = []      # 読みが決まらなかった漢字語
        self.straddle = []     # 複数ノードにまたがって付けられなかった語
        self.alignfail = []    # 位置合わせに失敗してまとめて付けた語

    def block_assignments(self, text):
        """ブロックの文字列に対する [(開始, 終了, 読み)]（開始・終了は text 上の位置、コードポイント）"""
        taken = []   # 既に決まった範囲（上書き・規則）
        out = []

        def overlaps(a, b):
            return any(a < tb and ta < b for ta, tb in taken)

        for surface, target, reading in self.overrides:
            for m in re.finditer(re.escape(surface), text):
                if overlaps(m.start(), m.end()):
                    continue
                ts = m.start() + surface.index(target)
                al = align(target, reading)
                if al is None:
                    out.append((ts, ts + len(target), reading))
                else:
                    out.extend((ts + a, ts + b, r) for a, b, r in al)
                taken.append((m.start(), m.end()))
        for a, b, reading in counter_assignments(text):
            if not overlaps(a, b):
                out.append((a, b, reading))
                taken.append((a, b))

        # 決まった範囲は伏せて解析する（重なった語を丸ごと捨てて、残りの漢字が覆われなくなるのを防ぐ）
        masked = list(text)
        for ta, tb in taken:
            masked[ta:tb] = ['・'] * (tb - ta)
        masked = ''.join(masked)

        pos = 0
        for w in self.tagger(masked):
            surface = w.surface
            start = masked.find(surface, pos)
            if start < 0:
                continue
            end = start + len(surface)
            pos = end
            if not KANJI_RE.search(surface) or overlaps(start, end):
                continue
            kana = getattr(w.feature, 'kana', None)
            if not kana or kana == '*':
                self.missing.append(surface)
                continue
            al = align(surface, kana)
            if al is None:
                self.alignfail.append((surface, kana))
                out.append((start, end, kata2hira(kana)))
            else:
                out.extend((start + a, start + b, r) for a, b, r in al)
        return out

    def analyze_block(self, nodes):
        """ブロックのノード列 -> {ノード文字列: [[開始, 長さ, 読み], ...]}（UTF-16単位）"""
        text = ''.join(nodes)
        if not KANJI_RE.search(text):
            return {}
        assigns = sorted(self.block_assignments(text))
        result, offset = {}, 0
        bounds = []
        for n in nodes:
            bounds.append((offset, offset + len(n)))
            offset += len(n)
        per_node = [[] for _ in nodes]
        for a, b, r in assigns:
            hit = [i for i, (s, e) in enumerate(bounds) if s <= a and b <= e]
            if hit:
                i = hit[0]
                s = bounds[i][0]
                per_node[i].append([utf16_pos(nodes[i], a - s), utf16_pos(nodes[i], b - s) - utf16_pos(nodes[i], a - s), r])
            else:
                self.straddle.append(text[a:b])
        for n, spans in zip(nodes, per_node):
            if spans:
                result.setdefault(n, spans)
        return result


def build_page_dict(html_text, analyzer):
    blocks, all_nodes = collect_blocks(html_text)
    entries, conflicts = {}, []
    for nodes in blocks:
        for n, spans in analyzer.analyze_block(nodes).items():
            k = node_key(n)
            if k in entries and entries[k] != spans:
                conflicts.append(n)
                continue
            entries.setdefault(k, spans)
    return {'v': 1, 'n': entries}, all_nodes, conflicts


def uncovered_kanji(all_nodes, dictionary):
    """辞書のルビで覆われていない漢字を返す"""
    bad = []
    for n in all_nodes:
        if not KANJI_RE.search(n):
            continue
        spans = dictionary['n'].get(node_key(n), [])
        covered = set()
        for s, l, _ in spans:
            covered.update(range(s, s + l))
        u16 = n.encode('utf-16-le')
        pos = 0
        for ch in n:
            w = len(ch.encode('utf-16-le')) // 2
            if is_kanji(ch) and not any(p in covered for p in range(pos, pos + w)):
                bad.append((ch, n[max(0, n.index(ch) - 6): n.index(ch) + 6]))
            pos += w
    return bad


# ---------------------------------------------------------------- ページとファイル
def resolve_pages(patterns):
    pages = []
    for pat in patterns:
        hits = sorted(ROOT.glob(pat))
        if not hits:
            raise SystemExit('見つかりません: ' + pat)
        pages.extend(hits)
    return pages


def dict_path_for(page):
    return DICT_DIR / (page.stem + '.json')


def rel_url(from_page, to_file):
    import os
    return os.path.relpath(to_file, from_page.parent).replace(os.sep, '/')


def ensure_body_attr(page, html_text):
    """<body> に data-furigana を付ける（無ければ追加、あれば値を更新）"""
    value = rel_url(page, dict_path_for(page))
    m = re.search(r'<body([^>]*)>', html_text)
    if not m:
        raise SystemExit('<body> が見つかりません: %s' % page)
    attrs = m.group(1)
    if re.search(r'data-furigana="[^"]*"', attrs):
        new_attrs = re.sub(r'data-furigana="[^"]*"', 'data-furigana="%s"' % value, attrs)
    else:
        new_attrs = attrs + ' data-furigana="%s"' % value
    if new_attrs == attrs:
        return html_text, False
    return html_text[:m.start()] + '<body%s>' % new_attrs + html_text[m.end():], True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('pages', nargs='*', default=DEFAULT_PAGES, help='対象ページ（既定: ITパスポートの全ページ）')
    ap.add_argument('--list', action='store_true', help='単語と読みの一覧（レビュー用）を表示して終了（ファイルは書かない）')
    ap.add_argument('--check', action='store_true', help='辞書で覆えない漢字の数を調べる（ファイルは書かない）')
    args = ap.parse_args()

    analyzer = Analyzer()
    pages = resolve_pages(args.pages)
    listing, total_uncovered = {}, 0
    for page in pages:
        html_text = page.read_text(encoding='utf-8')
        dictionary, all_nodes, conflicts = build_page_dict(html_text, analyzer)
        for k, spans in dictionary['n'].items():
            pass
        if args.check:
            path = dict_path_for(page)
            if not path.exists():
                print('辞書がありません:', path.relative_to(ROOT))
                total_uncovered += sum(1 for n in all_nodes for c in n if is_kanji(c))
                continue
            stored = json.loads(path.read_text(encoding='utf-8'))
            bad = uncovered_kanji(all_nodes, stored)
            stale = dictionary['n'] != stored['n']
            print('%s: 覆えない漢字 %d%s' % (page.relative_to(ROOT), len(bad), '（辞書が古い：再生成してください）' if stale else ''))
            for ch, ctx in bad[:5]:
                print('   ', ch, '…', ctx.replace('\n', ' '))
            total_uncovered += len(bad) + (1 if stale else 0)
            continue
        # 一覧（表記→読みの数）
        blocks, _ = collect_blocks(html_text)
        for nodes in blocks:
            text = ''.join(nodes)
            for a, b, r in analyzer.block_assignments(text):
                listing.setdefault(text[a:b], {}).setdefault(r, 0)
                listing[text[a:b]][r] += 1
        if args.list:
            continue
        path = dict_path_for(page)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(dictionary, ensure_ascii=False, separators=(',', ':'), sort_keys=True), encoding='utf-8')
        new_html, changed = ensure_body_attr(page, html_text)
        if changed:
            page.write_text(new_html, encoding='utf-8')
        print('%s -> %s（%d件, %s）%s' % (page.relative_to(ROOT), path.relative_to(ROOT), len(dictionary['n']),
                                       '%.1fKB' % (path.stat().st_size / 1024), ' ＋body属性を更新' if changed else ''))
        if conflicts:
            print('  同じ文でも文脈で読みが違った（最初を採用）:', len(conflicts))

    if args.check:
        print('uncovered kanji: %d' % total_uncovered)
        sys.exit(1 if total_uncovered else 0)
    if args.list:
        for surface in sorted(listing):
            readings = listing[surface]
            warn = '  ★読みが複数' if len(readings) > 1 else ''
            print('%s\t%s%s' % (surface, ' / '.join('%s(%d)' % (r, c) for r, c in sorted(readings.items(), key=lambda x: -x[1])), warn))
    if analyzer.missing:
        print('★読みが決まらなかった語:', sorted(set(analyzer.missing)), file=sys.stderr)
    if analyzer.straddle:
        print('★複数のタグにまたがって付けられなかった語:', sorted(set(analyzer.straddle)), file=sys.stderr)
    if analyzer.alignfail:
        print('★漢字と送り仮名の位置合わせに失敗（まとめて付けた）:', sorted(set(analyzer.alignfail)), file=sys.stderr)


if __name__ == '__main__':
    main()
