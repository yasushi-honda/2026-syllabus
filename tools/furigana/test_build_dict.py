#!/usr/bin/env python3
"""build_dict.py のテスト。 tools/furigana/.venv/bin/python tools/furigana/test_build_dict.py"""
import unittest

import build_dict as bd


def spans_text(html, analyzer=None):
    """HTML -> [(ルビを付けた文字列, 読み)] （ブロックごとの結果を平坦にしたもの）"""
    analyzer = analyzer or bd.Analyzer(overrides=[])
    blocks, _ = bd.collect_blocks(html)
    out = []
    for nodes in blocks:
        for n, spans in analyzer.analyze_block(nodes).items():
            u = n.encode('utf-16-le')
            for s, l, r in spans:
                out.append((u[s * 2:(s + l) * 2].decode('utf-16-le'), r))
    return out


class AlignTest(unittest.TestCase):
    def test_okurigana(self):
        self.assertEqual(bd.align('受け取る', 'ウケトル'), [(0, 1, 'う'), (2, 3, 'と')])

    def test_pure_kanji(self):
        self.assertEqual(bd.align('脅威', 'キョウイ'), [(0, 2, 'きょうい')])

    def test_trailing_okurigana(self):
        self.assertEqual(bd.align('攻める', 'セメル'), [(0, 1, 'せ')])

    def test_mismatch_returns_none(self):
        self.assertIsNone(bd.align('受け取る', 'ホゲ'))


class CollectTest(unittest.TestCase):
    def test_excluded_elements_are_skipped(self):
        html = '<p>脅威<code>攻撃</code>とは<script>var x="漢字";</script></p><pre>標的</pre><svg><text>図</text></svg>'
        _, nodes = bd.collect_blocks(html)
        self.assertEqual(nodes, ['脅威', 'とは'])

    def test_data_no_furigana(self):
        _, nodes = bd.collect_blocks('<p>脅威<span data-no-furigana>攻撃</span>です</p>')
        self.assertEqual(nodes, ['脅威', 'です'])

    def test_inline_tags_join_into_one_block(self):
        blocks, _ = bd.collect_blocks('<p>標的<strong>型</strong>攻撃</p>')
        self.assertEqual(blocks, [['標的', '型', '攻撃']])

    def test_block_tags_split(self):
        blocks, _ = bd.collect_blocks('<ul><li>脅威</li><li>攻撃</li></ul>')
        self.assertEqual(blocks, [['脅威'], ['攻撃']])

    def test_head_is_excluded(self):
        _, nodes = bd.collect_blocks('<html><head><title>標題</title></head><body><p>本文</p></body></html>')
        self.assertEqual(nodes, ['本文'])

    def test_entities_are_decoded(self):
        _, nodes = bd.collect_blocks('<p>A&amp;B 漢字</p>')
        self.assertEqual(nodes, ['A&B 漢字'])


class ReviewFixesTest(unittest.TestCase):
    def test_comment_splits_text_nodes_like_browsers(self):
        _, nodes = bd.collect_blocks('<p>標的<!-- 確認日 -->型</p>')
        self.assertEqual(nodes, ['標的', '型'])

    def test_option_is_excluded(self):
        _, nodes = bd.collect_blocks('<select><option>選択</option></select><p>本文</p>')
        self.assertEqual(nodes, ['本文'])

    def test_third_person_is_not_a_counter(self):
        r = spans_text('<p>3人称と3人</p>')
        self.assertNotIn(('3人', 'ひとり'), r)
        self.assertIn(('人', 'にん'), r)

    def test_fullwidth_digits_do_not_crash(self):
        spans_text('<p>１０分と２人</p>')   # 全角数字は規則の対象外（MeCabに任せる）

    def test_dynamic_texts_are_in_every_dictionary(self):
        d, _, _ = bd.build_page_dict('<p>本文</p>', bd.Analyzer(overrides=[]))
        for t in bd.DYNAMIC_TEXTS:
            self.assertIn(bd.node_key(t), d['n'], t)


class KeyTest(unittest.TestCase):
    def test_known_value(self):
        # app.js の nodeKey と同じ値になること（FNV-1a 32bit、UTF-16単位）。'a' = 0xe40c292c
        self.assertEqual(bd.node_key('a'), 'e40c292c.1')

    def test_length_counts_utf16_units(self):
        self.assertTrue(bd.node_key('𠮟').endswith('.2'))


class AnalyzeTest(unittest.TestCase):
    def test_reading_in_context(self):
        r = dict(spans_text('<p>標的型攻撃の脆弱性</p>'))
        self.assertEqual(r.get('標的'), 'ひょうてき')
        self.assertEqual(r.get('型'), 'がた')          # 連濁（単独の「型」はかた）
        self.assertIn('攻撃', r)

    def test_inline_tag_keeps_context(self):
        r = spans_text('<p>標的<strong>型</strong>攻撃</p>')
        self.assertIn(('型', 'がた'), r)

    def test_okurigana_is_not_annotated(self):
        r = spans_text('<p>情報を受け取る</p>')
        self.assertIn(('受', 'う'), r)
        self.assertIn(('取', 'と'), r)

    def test_kana_only_has_no_ruby(self):
        self.assertEqual(spans_text('<p>これはテストです</p>'), [])

    def test_override_wins(self):
        a = bd.Analyzer(overrides=[('脆弱性', '脆弱性', 'ぜいじゃくせい')])
        self.assertIn(('脆弱性', 'ぜいじゃくせい'), spans_text('<p>脆弱性を直す</p>', a))

    def test_override_partial_target(self):
        a = bd.Analyzer(overrides=[('1つ目', '目', 'め')])
        self.assertIn(('目', 'め'), spans_text('<p>1つ目</p>', a))

    def test_counter_minutes(self):
        r = spans_text('<p>10分と5分と3分野</p>')
        self.assertIn(('分', 'ぷん'), r)
        self.assertIn(('分', 'ふん'), r)
        self.assertNotIn(('分', 'ぷん'), [x for x in r if x[0] == '分'][2:])  # 3分野の「分」にはぷんを付けない

    def test_counter_dates(self):
        r = spans_text('<p>10月7日に試験</p>')
        self.assertIn(('月', 'がつ'), r)
        self.assertIn(('7日', 'なのか'), r)

    def test_counter_persons(self):
        r = spans_text('<p>1人と2人と5人</p>')
        self.assertIn(('1人', 'ひとり'), r)
        self.assertIn(('2人', 'ふたり'), r)
        self.assertIn(('人', 'にん'), r)

    def test_surrogate_pair_positions(self):
        # 絵文字（サロゲートペア）を含む文章でも、位置が UTF-16 の単位になること
        r = spans_text('<p>😀脅威</p>')
        a = bd.Analyzer(overrides=[])
        blocks, _ = bd.collect_blocks('<p>😀脅威</p>')
        res = a.analyze_block(blocks[0])
        self.assertEqual(res['😀脅威'][0][0], 2)

    def test_same_text_dedupes(self):
        d, _, conflicts = bd.build_page_dict('<p>脅威</p><p>脅威</p>', bd.Analyzer(overrides=[]))
        dynamic = {bd.node_key(t) for t in bd.DYNAMIC_TEXTS}
        self.assertEqual(len(set(d['n']) - dynamic), 1)   # 同じ文は1件にまとまる
        self.assertEqual(conflicts, [])


class CoverageTest(unittest.TestCase):
    def test_covered_has_zero_uncovered(self):
        a = bd.Analyzer(overrides=[])
        d, nodes, _ = bd.build_page_dict('<p>標的型攻撃の脆弱性を受け取る</p>', a)
        self.assertEqual(bd.uncovered_kanji(nodes, d), [])

    def test_missing_dictionary_entry_is_reported(self):
        bad = bd.uncovered_kanji(['脅威'], {'v': 1, 'n': {}})
        self.assertEqual([c for c, _ in bad], ['脅', '威'])


class BodyAttrTest(unittest.TestCase):
    def test_idempotent(self):
        from pathlib import Path
        page = bd.COURSE_DIR / 'week99.html'
        html = '<html><body class="x"><p>a</p></body></html>'
        h1, changed1 = bd.ensure_body_attr(page, html)
        h2, changed2 = bd.ensure_body_attr(page, h1)
        self.assertTrue(changed1)
        self.assertFalse(changed2)
        self.assertEqual(h1, h2)
        self.assertIn('data-furigana="furigana/week99.json"', h1)


if __name__ == '__main__':
    unittest.main(verbosity=1)
