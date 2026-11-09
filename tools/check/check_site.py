#!/usr/bin/env python3
"""公開サイトの静的チェック（PRで自動実行）。標準ライブラリのみ。

検査項目（HTMLごと）:
  1. id の重複がない
  2. data-md-source（コピーボタン）の id が同じファイルに存在する
  3. ローカルの href / src（相対パス）が実在する
使い方: python3 tools/check/check_site.py [ファイル...]（省略時は全HTML）
終了コード: 問題があれば 1
"""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".venv", "node_modules", ".playwright-mcp"}


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.sources, self.links = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if a.get("data-md-source"):
            self.sources.append(a["data-md-source"])
        for k in ("href", "src"):
            v = a.get(k)
            if v:
                self.links.append(v)


def is_local(v):
    p = urlparse(v)
    return not p.scheme and not p.netloc and v[0] not in "#?" and not v.startswith("//")


def check(path):
    errs = []
    s = Scan()
    s.feed(path.read_text(encoding="utf-8"))
    seen = set()
    for i in s.ids:
        if i in seen:
            errs.append(f"id重複: {i}")
        seen.add(i)
    for src in s.sources:
        if src not in seen:
            errs.append(f"コピー対象のidが無い: {src}")
    for v in s.links:
        if not is_local(v):
            continue
        t = (path.parent / unquote(urlparse(v).path)).resolve()
        if not t.exists():
            errs.append(f"リンク先が無い: {v}")
    return errs


def main(argv):
    files = [Path(a).resolve() for a in argv] or [
        p for p in ROOT.rglob("*.html") if not (set(p.relative_to(ROOT).parts) & SKIP_DIRS)
    ]
    bad = 0
    for f in sorted(files):
        try:
            name = f.relative_to(ROOT)
        except ValueError:
            name = f
        for e in check(f):
            print(f"NG {name}: {e}")
            bad += 1
    print(f"{len(files)}ファイルを検査、問題 {bad} 件")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
