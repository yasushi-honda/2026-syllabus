---
updated: 2026-07-21
---

## 現在のミッション
プログラム基礎I（program-basics.html）の学期終盤スケジュールを、当初の全15回想定から「今回（week13）を含めてあと2回」で終わる全14回構成に圧縮し、week13〜14の詳細ページを新規作成する。

## 背景・why
担当教員（decision-maker）から「火曜1・2限（プログラム基礎I）の今回を含めてあと2回、次回が最終」と相談を受けた。親ページには当初「デバッグ集中回(13)→自由制作(14)→仕上げ＆振り返り(15)」の全15回想定が既に書かれていたが、詳細ページはweek12までしか作成されていなかった。AIコミュニケーション基礎（PR #152）・AI活用プログラミング基礎（PR #146）と同様の「終盤圧縮」パターンだが、AIコミュニケーション基礎は既にweek13-14が完結済みだったため対象外とし、本科目のみが対象と判明した。

week13「デバッグ集中回（AIなしで直す）」はweek12の次回予告と一致するためそのまま維持し、week14で旧14「自由制作」＋旧15「仕上げ＆振り返り」を統合して最終回とした。

## 完了の定義
- `program-basics.html` の授業計画表が「全14回」表記になり、week13・14の2行に再編されている（証明: `grep -c "全15回" program-basics.html` が0）
- `program-basics/week01.html` の「全15回」表記が「全14回」に同期されている（証明: `grep -c "全15回" program-basics/week01.html` が0）
- `program-basics/week13.html`, `week14.html` が新規作成され、各タイムライン合計が180分（40+50+50+30+10、休憩10分除く）である
- `program-basics/week12.html` の lesson-nav「次の回」がweek13.htmlへのリンクに有効化されている
- `content/program-basics.md` の授業計画セクションがHTMLと整合している
- `CLAUDE.md` のファイル構成表に新規2ファイル（week13/14.html）が記載されている
- `/code-review medium` でConfirmed指摘が0件、またはすべて解消済み
- マージ後、5ページ（program-basics.html, week01/12/13/14.html）が本番URLでHTTP 200（証明: curl）

## 進行中のtasks
- [x] 対象科目・回数構成のヒアリング（火曜=プログラム基礎I / AIコミュ基礎の2択→プログラム基礎Iのみと確定、AIコミュ基礎は既完結を確認）
- [x] plan mode でのフルプラン作成・承認（6ファイル変更のため）
- [x] program-basics/week13.html 新規作成（デバッグ集中回・AIなしで直す）
- [x] program-basics/week14.html 新規作成（自由制作＆振り返り・前期最終回）
- [x] program-basics.html 授業計画表の再編（全14回化、week13-14の2行化、圧縮注記追加）
- [x] program-basics/week12.html lesson-nav「次の回」有効化
- [x] content/program-basics.md, CLAUDE.md ファイル構成表の同期
- [x] `/code-review medium`（8角度・並列verify）実行、Confirmed 2件（week14の週参照誤り・week01の全15回残存）を修正
- [x] コミット・PR #156作成・マージ・デプロイ確認（2026-07-21マージ・デプロイ・本番200確認済み）

## 🔄 中断点（in-flight）
なし
