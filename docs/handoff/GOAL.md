---
updated: 2026-07-14
---

## 現在のミッション
AIコミュニケーション基礎（ai-communication.html）の学期終盤スケジュールを、当初の全15回想定から「week12（実施済み）を含めて残り3回（week12〜14）」に圧縮し、week13〜14の詳細ページを新規作成する。

## 背景・why
担当教員（decision-maker）から「火曜日の授業が14回までしかなかった」と相談を受けた。当初の全15回想定のうち1回減。week12は実施済み・ページ作成済み（PR #151, 2026-07-14マージ）。旧シラバスのweek13(個人課題：制作)〜week14(AI育成②：知識の体系化)〜week15(仕上げ＆振り返り、発表なし)の3ステップを、実施可能な2回（week13〜14）に収める必要がある。木曜日科目ai-programmingで先日行った同種の圧縮（PR #146）と異なり、この科目の評価方法には発表要件がないため、最終発表会の統合は不要（「発表なし」の性質を維持する）。

week12.htmlの本文中に「残り4回（第12〜15回）」という前提の記述が複数箇所（テーマ概要・大事な前提ブロック・タイムライン本文）に残っており、圧縮後は事実と矛盾するため、week12.htmlの回数表記の修正も本ミッションのスコープに含む（学習データ⑪・内容の骨子は変更なし）。

## 完了の定義
- `ai-communication.html` の授業計画表が「全14回」表記になり、week13・14の2行に再編されている（証明: `grep -c "全15回" ai-communication.html` が0、`grep -c "全14回" ai-communication.html` が1以上、`grep -c "week13.html\|week14.html" ai-communication.html` が2以上）
- `ai-communication/week12.html` の回数表記矛盾が解消されている（証明: `grep -c "残り4回\|第12〜15回" ai-communication/week12.html` が0、`grep -c "lesson-nav-item--disabled" ai-communication/week12.html` が0）
- `ai-communication/week13.html`, `week14.html` が新規作成され、各タイムライン合計が180分（40+50+50+30+10、休憩10分除く）である（証明: 各ファイルのtimeline-durationを合算）
- `ai-communication/week14.html` の lesson-nav「次の回」が「前期最終回」disabled表記になっている（証明: `grep "前期最終回" ai-communication/week14.html` が1件以上）
- `content/ai-communication.md` の授業計画セクションがHTMLと整合している（証明: 目視diff）
- `CLAUDE.md` のファイル構成表に新規2ファイル（week13.html, week14.html）が記載されている
- code-reviewer + comment-analyzer 相当のレビューでCritical/Important指摘が0件、またはすべて解消済み
- マージ後、3ページ（ai-communication.html, week13.html, week14.html）が本番URLでHTTP 200（証明: curl）

## 進行中のtasks
- [x] ai-communication.html 授業計画表の再編（全14回化、week13-14の2行化、week15統合注記）
- [x] content/ai-communication.md 同期
- [x] ai-communication/week12.html 回数表記修正（残り4回→残り3回、第12〜15回→第12〜14回）+ lesson-nav「次の回」有効化
- [x] ai-communication/week13.html 新規作成（個人課題：制作、学習データ⑫）
- [x] ai-communication/week14.html 新規作成（AI育成②：仕上げ＆振り返り統合、学習データ⑬、発表なし）
- [x] CLAUDE.md ファイル構成表に新規2ファイル追記
- [x] レビュー（code-reviewer + comment-analyzer 並列）、指摘反映（week12残存2箇所修正、week01/week10/week11の波及「全15回→全14回」「第11〜15回→第11〜14回」修正、week14「一覧化」文言追加）
- [ ] コミット・PR作成・マージ・デプロイ確認（PR #152、追加修正コミット待ち）

## 🔄 中断点（in-flight）
なし
