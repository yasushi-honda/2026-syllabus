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
