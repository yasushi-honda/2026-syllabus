#!/usr/bin/env python3
"""make_qr.py のテスト。 tools/qr/.venv/bin/python tools/qr/test_make_qr.py"""
import re
import unittest

import make_qr as mq


class RenderTest(unittest.TestCase):
    URL = mq.SITE + 'it-passport-technology/week05.html'

    def test_same_url_gives_same_bytes(self):
        self.assertEqual(mq.render(self.URL), mq.render(self.URL))

    def test_different_url_gives_different_svg(self):
        self.assertNotEqual(mq.render(self.URL), mq.render(self.URL + '?w=5'))

    def test_svg_has_viewbox_and_matching_size(self):
        svg = mq.render(self.URL).decode('utf-8')
        m = re.search(r'viewBox="0 0 (\d+) (\d+)" width="(\d+)" height="(\d+)"', svg)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), m.group(3))
        self.assertEqual(m.group(2), m.group(4))
        self.assertEqual(m.group(1), m.group(2))  # 正方形

    def test_svg_is_self_contained(self):
        svg = mq.render(self.URL).decode('utf-8')
        self.assertNotIn('<script', svg)
        self.assertNotIn('http://', svg.replace('http://www.w3.org/2000/svg', ''))  # 外部参照なし
        self.assertIn('crispEdges', svg)

    def test_quiet_zone_is_at_least_4_modules(self):
        # 余白4モジュール: 最初の濃いセルは (4, 4) より内側から始まる
        svg = mq.render(self.URL).decode('utf-8')
        d = re.search(r'class="qrline"[^>]*d="M(\d+(?:\.\d+)?) (\d+(?:\.\d+)?)', svg)
        self.assertIsNotNone(d)
        self.assertGreaterEqual(float(d.group(1)), 4)
        self.assertGreaterEqual(float(d.group(2)), 4)


class ListTest(unittest.TestCase):
    def test_manifest_is_valid(self):
        rows = mq.read_list()
        self.assertTrue(rows)
        outs = [o for o, _ in rows]
        self.assertEqual(len(outs), len(set(outs)), '出力パスの重複')
        for out, url in rows:
            self.assertTrue(out.endswith('.svg'), out)
            self.assertTrue(url.startswith(mq.SITE), url)

    def test_committed_files_are_up_to_date(self):
        # コミット済みの SVG が、いまのツールとマニフェストから作り直した結果と同じ
        for out, url in mq.read_list():
            path = mq.ROOT / out
            self.assertTrue(path.exists(), out + ' がありません（tools/qr/make_qr.py を実行）')
            self.assertEqual(path.read_bytes(), mq.render(url), out + ' が古いです（tools/qr/make_qr.py を実行）')


if __name__ == '__main__':
    unittest.main()
