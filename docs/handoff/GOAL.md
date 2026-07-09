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
- [ ] コミット・PR作成・マージ・デプロイ確認

## 🔄 中断点（in-flight）
なし
