# 2026年度 前期シラバス — 清風情報工科学院

## プロジェクト概要
担当4科目のシラバスをGitHub Pagesで公開する静的Webサイト。

- **公開URL**: https://yasushi-honda.github.io/2026-syllabus/
- **リポジトリ**: https://github.com/yasushi-honda/2026-syllabus

## 技術スタック
- 静的HTML/CSS/JS（フレームワークなし）
- GitHub Actions → GitHub Pages（mainブランチpush時に自動デプロイ）

## ファイル構成
```
index.html              # トップページ（時間割＋4科目カード）
program-basics.html     # プログラム基礎 I（火1・2限）
ai-communication.html   # AIコミュニケーション基礎（火3・4限）
natural-language-dev.html # 自然言語開発（木1・2限）
ai-programming.html     # AI活用プログラミング基礎（木3・4限）※AIコミュ基礎と共通ベース
styles.css              # 共通スタイル
app.js                  # Markdownコピー機能等
content/                # Markdownソース（コピーボタン用）
.github/workflows/      # GitHub Pagesデプロイ設定
```

## 運用ルール
- 4科目共通のデザイン・レイアウトを維持する
- 科目ごとのテーマカラー: blue(プログラム基礎), purple(AIコミュ), green(自然言語開発), orange(AI活用プログラミング)
- HTML変更時は対応するcontent/*.mdも同期する
