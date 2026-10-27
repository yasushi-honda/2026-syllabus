#!/usr/bin/env python3
"""週ページ・ゲームに載せる QR コード（静的な SVG）を作る。

使い方（リポジトリのルートで）:
  tools/qr/.venv/bin/python tools/qr/make_qr.py          # qr_list.tsv の全件を作る（既存は上書き）
  tools/qr/.venv/bin/python tools/qr/make_qr.py --check  # 作り直した結果と、いまのファイルが同じか確かめる（違えば終了コード1）

QR は事前に SVG にして HTML に <img> で埋め込む。実行時の外部ライブラリ・CDN は使わない
（学校のネットワークで失敗しない／ブラウザ翻訳の影響を受けない）。
URL を変えたら qr_list.tsv を直して、このツールを実行し直す。

初回: python3 -m venv tools/qr/.venv && tools/qr/.venv/bin/pip install -r tools/qr/requirements.txt
"""
import io
import re
import sys
from pathlib import Path

import segno

ROOT = Path(__file__).resolve().parents[2]
LIST = Path(__file__).with_name('qr_list.tsv')
SITE = 'https://yasushi-honda.github.io/2026-syllabus/'

# 誤り訂正 M（約15%）。余白（クワイエットゾーン）は規格どおり4モジュール以上。濃い灰色と白で、コントラストを十分にとる。
ERROR = 'm'
BORDER = 4
DARK = '#1b1b1b'
LIGHT = '#ffffff'


def read_list():
    """qr_list.tsv の行 -> [(出力パス, URL)]。# で始まる行と空行は無視する。"""
    rows = []
    for n, line in enumerate(LIST.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        parts = line.split('\t')
        if len(parts) != 2:
            raise SystemExit('%s:%d: 「出力パス<TAB>URL」の2列にしてください: %r' % (LIST.name, n, line))
        out, url = parts[0].strip(), parts[1].strip()
        if not url.startswith(SITE):
            raise SystemExit('%s:%d: URL は公開サイト（%s）の中だけにしてください: %s' % (LIST.name, n, SITE, url))
        rows.append((out, url))
    return rows


def render(url):
    """URL -> SVG（bytes）。同じ URL なら同じバイト列になる（--check のため）。"""
    qr = segno.make(url, error=ERROR, micro=False)
    buf = io.BytesIO()
    qr.save(buf, kind='svg', scale=1, border=BORDER, dark=DARK, light=LIGHT, xmldecl=False, svgns=True, nl=False)
    svg = buf.getvalue().decode('utf-8')
    # segno の SVG は width/height だけで viewBox がない。<img> を CSS で拡大縮小しても崩れないよう viewBox を足し、
    # 細い線のすき間が出ないよう crispEdges を指定する
    m = re.search(r'<svg xmlns="http://www.w3.org/2000/svg" width="(\d+)" height="(\d+)"', svg)
    if not m:
        raise SystemExit('segno の出力の形が想定と違います（svg の開始タグ）')
    svg = svg.replace(m.group(0), '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s"' % (m.group(1), m.group(2), m.group(1), m.group(2)), 1)
    if svg.count('<path class="qrline"') != 1:
        raise SystemExit('segno の出力の形が想定と違います（qrline のパス）')
    svg = svg.replace('<path class="qrline"', '<path shape-rendering="crispEdges" class="qrline"', 1)
    return svg.encode('utf-8')


def main(argv):
    check = '--check' in argv
    rows = read_list()
    if not rows:
        raise SystemExit('qr_list.tsv に行がありません')
    seen, bad = set(), 0
    for out, url in rows:
        if out in seen:
            raise SystemExit('出力パスが重複しています: ' + out)
        seen.add(out)
        path = ROOT / out
        svg = render(url)
        if check:
            same = path.exists() and path.read_bytes() == svg
            print('%s  %s' % ('OK  ' if same else 'DIFF', out))
            bad += 0 if same else 1
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(svg)
            print('作成 %s（%d バイト） <- %s' % (out, len(svg), url))
    if check:
        print('違いがあるファイル: %d' % bad)
        return 1 if bad else 0
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
