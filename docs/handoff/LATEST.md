# アーカイブ済みミッション履歴

GOAL.mdを別ゴールで置き換える際、旧ミッション全文をここに転記する（アーカイブ経路がないGOAL.mdの上書き消失防止）。

---

## [2026-07-16 完了] 自然言語開発 学期終盤スケジュール拡張

```markdown
---
updated: 2026-07-16
---

## 現在のミッション
自然言語開発（natural-language-dev.html）の学期終盤スケジュールを、当初の全15回想定から「今回（week14）を含めてあと3回」で終わる全16回構成に拡張し、week14〜16の詳細ページを新規作成する。

## 背景・why
担当教員（decision-maker）から「木曜1・2限（自然言語開発）の今回を含めてあと3回作ってほしい」と相談を受けた。逆算の結果、本日2026-07-16の授業回が当初計画のweek14に該当し（week13は2026-07-09実施済み）、当初全15回想定に対し1回多い全16回で構成されることが判明した。ai-communication（PR #152）・ai-programming（PR #146）は同学期で「全15回→14回への圧縮」だったが、本科目は新設科目で対象学年・専攻（IT・情報処理専攻(システム)3年次）が異なり、「全15回→16回への拡張」になった点が異なる。

旧week14「プロジェクト最終仕上げ」（1回分の内容）をweek14「最終調整・テスト」とweek15「ドキュメント整備・発表準備」の2回に分割し、旧week15「成果発表＆総括」をweek16として新規作成した。

## 完了の定義
- `natural-language-dev.html` の授業計画表が「全16回」表記になり、week14・15・16の3行に再編されている（証明: `grep -c "全15回" natural-language-dev.html` が0、`grep -c "全16回" natural-language-dev.html` が1以上、`grep -c "week14.html\|week15.html\|week16.html" natural-language-dev.html` が3以上）
- `natural-language-dev/week01.html` の「全15回」表記が「全16回」に同期されている（証明: `grep -c "全15回" natural-language-dev/week01.html` が0）
- `natural-language-dev/week14.html`, `week15.html`, `week16.html` が新規作成され、各タイムライン合計が180分（40+50+50+30+10、休憩10分除く）である
- `natural-language-dev/week13.html` の lesson-nav「次の回」がweek14.htmlへのリンクに有効化されている
- `content/natural-language-dev.md` の授業計画セクションがHTMLと整合している（証明: 目視diff）
- `CLAUDE.md` のファイル構成表に新規3ファイル（week14/15/16.html）が記載されている
- code-reviewer + 事実確認レビューでCritical/Important指摘が0件、またはすべて解消済み
- マージ後、5ページ（natural-language-dev.html, week13〜16.html）が本番URLでHTTP 200（証明: curl）

## 進行中のtasks
- [x] 対象科目・回数構成のヒアリング（自然言語開発=全16回拡張、ai-programming=対応済み確認）
- [x] natural-language-dev/week14.html 新規作成（プロジェクト最終仕上げ①：最終調整・テスト）
- [x] natural-language-dev/week15.html 新規作成（プロジェクト最終仕上げ②：ドキュメント整備・発表準備）
- [x] natural-language-dev/week16.html 新規作成（成果発表＆総括）
- [x] natural-language-dev.html 授業計画表の再編（全16回化、week14-16の3行化）
- [x] natural-language-dev/week13.html lesson-nav「次の回」有効化・次回予告文言更新
- [x] natural-language-dev/week01.html「全15回」表記2箇所を「全16回」に同期
- [x] content/natural-language-dev.md, CLAUDE.md ファイル構成表の同期
- [x] レビュー（code-reviewer + 事実確認 並列）、指摘反映（week14見出し「最終回」矛盾表現削除、week12.html旧テーマ名同期、week16参考リンク追加等）
- [x] コミット・PR作成・マージ・デプロイ確認（PR #154, 2026-07-16マージ・デプロイ・本番200確認済み）

## 🔄 中断点（in-flight）
なし
```

---

## [2026-07-14 完了] AIコミュニケーション基礎 学期終盤スケジュール圧縮

```markdown
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
- [x] コミット・PR作成・マージ・デプロイ確認（PR #152, 2026-07-14マージ・デプロイ・本番200確認済み）

## 🔄 中断点（in-flight）
なし
```

---

## [2026-07-09 完了] AI活用プログラミング基礎 学期終盤スケジュール圧縮

```markdown
---
updated: 2026-07-09
---

## 現在のミッション
AI活用プログラミング基礎（ai-programming.html）の学期終盤スケジュールを、当初の全15回想定から「week11（今日実施済み）を含めて残り4回（week11〜14）」に圧縮し、week12〜14の詳細ページを新規作成する。

## 背景・why
担当教員（decision-maker）から「今回(week11)含めてあと4回だが、今の内容だと足りない」と相談を受けた。旧シラバスのweek12〜15（個人テーマ決定→制作→仕上げ→発表準備→最終発表会の5ステップ）を、実施可能な4回（week11〜14）に収める必要がある。評価方法に「学期末の発表の機会」が明記されているため、最終発表会（旧week15相当）はweek14に統合する形で必ず残す。想定学生数は約20〜30人。

## 完了の定義
- `ai-programming.html` の授業計画表がweek12〜14の3行に再編され、week15の単独記述が残っていない（証明: `grep -c "week15\|第15回" ai-programming.html` が0、`grep -c "week12.html\|week13.html\|week14.html" ai-programming.html` が3以上）
- `content/ai-programming.md` の授業計画セクションがHTMLと整合している（証明: 目視diff）
- `ai-programming/week12.html`, `week13.html`, `week14.html` が新規作成され、タイムライン合計が180分（40+50+50+30+10、休憩10分除く）である（証明: 各ファイルのtimeline-durationを合算）
- `ai-programming/week11.html` の lesson-nav「次の回」がweek12へのリンクに変わっている（証明: `grep "lesson-nav-item--disabled" ai-programming/week11.html` が0件）
- `CLAUDE.md` のファイル構成表に新規3ファイルが記載されている
- code-reviewer + comment-analyzer 相当のレビューでCritical/Important指摘が0件、またはすべて解消済み
- マージ後、4ページ（ai-programming.html, week12/13/14.html）が本番URLでHTTP 200（証明: curl）

## 進行中のtasks
- [x] ai-programming.html 授業計画表の再編（week12-14の3行化、week15統合注記）
- [x] content/ai-programming.md 同期
- [x] ai-programming/week12.html 新規作成（個人テーマを決めよう）
- [x] ai-programming/week13.html 新規作成（個人課題：探究・制作）
- [x] ai-programming/week14.html 新規作成（仕上げ＋最終発表会統合、人数別配分目安を含む）
- [x] ai-programming/week11.html の lesson-nav「次の回」有効化
- [x] CLAUDE.md ファイル構成表に新規3ファイル追記
- [x] レビュー（code-reviewer + comment-analyzer 並列）、指摘反映（既存週ページ01/02/08/09の「全15回」波及修正、week14内の時間表記矛盾修正、絵文字統一、人数目安追記、文言統一を実施）
- [x] コミット・PR作成・マージ・デプロイ確認（PR #146, 2026-07-09マージ・デプロイ・本番200確認済み）

## 🔄 中断点（in-flight）
なし
```
