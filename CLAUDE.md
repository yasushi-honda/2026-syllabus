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
program-basics/         # プログラム基礎 I の各回詳細ページ
  week01.html           #   第1回 オリエンテーション＆はじめてのHTML
  week02.html           #   第2回 HTMLの構造を学ぶ
ai-communication.html   # AIコミュニケーション基礎（火3・4限）
ai-communication/       # AIコミュニケーション基礎の各回詳細ページ
  week01.html           #   第1回 オリエンテーションとAI概論
  week02.html           #   第2回 「自分だけのAI」をつくろう
natural-language-dev.html # 自然言語開発（木1・2限）
natural-language-dev/   # 自然言語開発の各回詳細ページ
  week01.html           #   第1回 オリエンテーション＆前年度の進級制作を振り返る
  week02.html           #   第2回 コンテキストエンジニアリング入門
ai-programming.html     # AI活用プログラミング基礎（木3・4限）※AIコミュ基礎と共通ベース
ai-programming/         # AI活用プログラミング基礎の各回詳細ページ
  week01.html           #   第1回 オリエンテーション＆AIってなんだろう？
java-basics-1.html      # Java基礎I（土曜前期）
java-basics-2.html      # Java基礎II（土曜前期）
java-spring.html        # Javaフレームワーク（土曜後期）
java-teamdev.html       # チーム開発演習（土曜後期）
styles.css              # 共通スタイル（Editorial Paper Edition ライトテーマ）
app.js                  # Markdownコピー・タブ切替等
favicon.svg             # ファビコン
content/                # Markdownソース（コピーボタン用）
.github/workflows/      # GitHub Pagesデプロイ設定
```

## 運用ルール
- 4科目共通のデザイン・レイアウトを維持する
- 科目ごとのテーマカラー: blue(プログラム基礎), purple(AIコミュ), green(自然言語開発), orange(AI活用プログラミング)
- HTML変更時は対応するcontent/*.mdも同期する

---

## 各回詳細ページ作成プレイブック

新しい Week N の詳細ページを作るときは、このセクションに従う。時間配分ミス・リンク切れ・テンプレ逸脱を防ぐための固定ルール集。

### 科目 → テーマ色・配置対応表

| 科目 | 親ページ | 詳細ディレクトリ | テーマ色 | 時限 | 対象 |
|------|---------|----------------|---------|------|------|
| プログラム基礎 I | `program-basics.html` | `program-basics/` | `page-header--blue` | 火1・2限 | ITビジネスコース 2,3,4年次 |
| AIコミュニケーション基礎 | `ai-communication.html` | `ai-communication/` | `page-header--purple` | 火3・4限 | ITビジネスコース 2,3,4年次 |
| 自然言語開発 | `natural-language-dev.html` | `natural-language-dev/` | `page-header--green` | 木1・2限 | IT・情報処理専攻(システム) 3年次 |
| AI活用プログラミング基礎 | `ai-programming.html` | `ai-programming/` | `page-header--orange` | 木3・4限 | 情報系学科 1年次 |

### 科目別プロファイル（毎回参照する固有前提）

科目ごとに「対象学年」「学習データ系列の有無と密度」「NotebookLM/AIツールの導入時期」が異なる。週ページ生成前に必ずこの表で前提を確認すること。

| 科目 | 対象学年 | 学習データ系列 | NotebookLM導入 | 表現の注意 |
|------|---------|---------------|--------------|----------|
| プログラム基礎 I | ITビジネスコース 2,3,4年次（経験混在） | なし | — | HTML/CSS/JSの基礎、進度差を吸収する設計 |
| AIコミュニケーション基礎 | ITビジネスコース 2,3,4年次 | **①〜⑬（第1〜14回でほぼ毎回）** | 第1回で予告 → **第2回投入** | 「自分だけのAI」が核キーワード |
| 自然言語開発 | **IT・情報処理専攻(システム) 3年次** | なし | — | 前年度（2年次）進級制作の振り返りが通年の文脈起点 |
| AI活用プログラミング基礎 | **情報系学科 1年次** | **①〜④（第3/4/5/10回のみ）** | **第3回から** | 1年向けに丁寧。AIコミュ基礎の説明をそのまま流用しない |

- AIコミュ基礎とAI活用プログラミング基礎は「共通ベース」だが、**対象学年と密度が違う別科目**。文章のレベル・例示・専門用語の量を必ず調整する
- 学習データ番号は親ページの記述が正本。**勝手に振らない・ずらさない**

### 親ページ正本原則（Single Source of Truth）

各週ページの内容は、**親ページ（科目HTML）の該当週セルが正本**である。

- 親ページの「テーマ名」「主な内容・活動」「学習データ番号」「太字キーワード」は、週ページに必ず登場させる
- 週ページ生成時に親ページと矛盾が出たら、**週ページ側を直す**（親ページが正）
- 親ページの設計を変えたい場合は、**親ページを先に更新**してから週ページに反映する
- 週ページが既に存在する状態で親ページのテーマ・学習データ番号を変える場合、対応する週ページの該当箇所もセットで更新する

### 時間配分（固定・絶対厳守）

親ページの「2コマ連続（90分 + 90分 = 計180分）。途中休憩あり」は **休憩を枠外** とする宣言。タイムラインの合計は**休憩を除いて180分ちょうど**でなければならない。

| 区分 | 時間 | 備考 |
|------|------|------|
| 1限 前半 | **約40分** | オリエンテーション・授業全体方針 |
| 1限 後半 | **約50分** | 中核コンテンツ① |
| （休憩） | 10分 | **授業時間に含めない** |
| 2限 前半 | **約50分** | 中核コンテンツ② |
| 2限 後半 | **約30分** | 演習・発展 |
| まとめ | **約10分** | 次回予告・振り返り |
| **授業合計** | **180分** | 40+50+50+30+10 |

- この配分から逸脱する場合は、必ず親ページの宣言文も同時に書き換える
- レビューで「合計が180分を超える」と指摘されたら、**休憩10分を含めて数えていないか**を先に確認する（過去に誤ってこれで短縮した事例あり）

### 作業チェックリスト

```
□ 1. ブランチ作成: git checkout -b {subject-slug}-week{NN}
□ 2. ディレクトリ作成: mkdir -p {subject-slug}/
□ 3. 「科目別プロファイル」表で対象学年・学習データ系列・NotebookLM導入時期を確認
□ 4. 親ページの Week N 行を読み、以下を**逐語コピー**してメモ化（後で照合する正本）
       - テーマ名 / 主な内容・活動 / **【学習データN】の有無と内容** / 太字キーワード
□ 5. 既存 week01 を雛形としてコピー（同科目の前回 or 他科目の同週）
□ 6. page-header の class を対応表通りに変更（--blue/--purple/--green/--orange）
□ 7. 相対パス調整: ../styles.css, ../favicon.svg, ../app.js, ../index.html, ../{parent}.html
□ 8. breadcrumb を3階層に（シラバス一覧 / 科目名 / 第N回）
□ 9. page-badge は2つのみ（Week番号 + 時限）。他情報はページタイトル・親ページで既出
□ 10. タイムラインを固定配分（40/50/休/50/30/10）通りに設定
□ 11. 外部リンクを curl で事前検証（下記「リンク検証コマンド」）
□ 12. 本文を執筆（下記「既知の地雷リスト」を踏まないように）
□ 13. **整合性検証**: ステップ4のメモの全項目が週ページに登場するか grep で確認
       例: `grep -F "【学習データ①】" {dir}/week{NN}.html`
□ 14. 親ページの該当 Week セルを <a href="{dir}/week{NN}.html" class="week-link"> でリンク化
□ 15. このCLAUDE.mdの「ファイル構成」に新ファイルを追記
□ 16. git add / commit / push / PR作成
□ 17. レビュー実行: code-reviewer + comment-analyzer を並列で1回
□ 18. 指摘反映 → マージ → デプロイ成功確認（https URLで200確認）
```

### リンク検証コマンド

```bash
for u in URL1 URL2 URL3; do
  printf '%-70s ' "$u"
  curl -s -o /dev/null -w "%{http_code}\n" -L -A "Mozilla/5.0" "$u"
done
```

- 200以外が返ったら原則差し替え
- ただし **Gemini (`gemini.google.com`) は curl では 502** が返る（Google側のbot対策）。ブラウザでは正常動作するため例外として採用可

### 既知の地雷リスト（過去PRレビュー由来）

| 地雷 | 正解 | 出典 |
|------|------|------|
| `education.github.com/benefits` は廃止（301リダイレクト） | `education.github.com/pack` を使う | PR #37 |
| MDN 旧URL `/Web/HTML/Element` は301 | `/Web/HTML/Reference/Elements` を使う | PR #37 |
| 「GitHub Copilot」曖昧 | 「**Copilot Student**」と正式名称で | PR #37 |
| 「Codespacesの拡張枠」曖昧 | 「**月180コア時間枠**」と具体値 | PR #37 |
| Live Server を Codespaces 標準機能のように書く | 「**`python3 -m http.server` → 自動ポート転送 → Simple Browser**」の3ステップで明記する。`file://` では Simple Browser がレンダリングしないため**サーバー起動手順の省略禁止**。詰まった場合のフォールバックとして「Copilot Chat に『index.html をブラウザで開いて』と頼む」を併記する | PR #37, 教室実地フィードバック |
| NotebookLM/WS Education を「設定可能」と書く | 「**Core Service としてデフォルトで学習に使われない**」 | PR #38 |
| 「次に来る単語を予測」 | 「**次に来る言葉の断片（トークン）を予測**」 | PR #38 |
| Workspace for Education URL が `ALL_us`（英語） | `ALL_jp` の日本語版を使う | PR #38 |
| 「第N回で〜」の具体週番号ハードコード | 「**後半の回で**」等に弱める＋同期マーカーコメント | PR #38 |
| Gemini UI「真ん中に質問欄」等の具体配置記述 | 「**画面下部の入力欄**」程度に抑え、UI変更に備え口頭確認に委ねる | PR #39 |
| 個人情報禁止を**ルールのみ**提示 | 「**入力はAI改善に使われ得る**」等の**理由**を添える | PR #39 |
| 推奨ブラウザを Chrome/Edge のみに限定 | 「Chrome（学校PC）/ 自宅では Edge・Safari・Firefox も可」 | PR #39 |
| バッジを3つ以上配置 | **2つ**（Week番号＋時限）に統一 | PR #39 |
| AIコミュ基礎の説明をAI活用プログラミングに流用（対象学年無視） | **科目別プロファイル表**で対象学年・密度を確認してから書く | 設計上の前提 |
| 学習データ番号(①〜⑬等)を勝手に振る/ずらす | 親ページの記述を**正本**として逐語参照する | 設計上の前提 |
| 親ページに無いキーワードを週ページに新規登場させる | 親ページを先に更新してから週ページに反映 | 設計上の前提 |

### レビュー手順（必ず実行）

1ファイルの小規模修正（時間値修正等）を除き、PR作成後は以下を **並列で1回** 実行:

- `pr-review-toolkit:code-reviewer` — テンプレート整合性・相対パス・HTML妥当性
- `pr-review-toolkit:comment-analyzer` — 事実の正確性・外部リンク生存・親ページ整合性

Criticalは必ず修正、Importantは原則修正、Suggestionは判断して採否決定。マージ後は https URLで HTTP 200 と表示を目視確認。

### 定期メンテナンス（半年〜1年に1回）

スキル化しても外部要因で陳腐化するため、以下を定期点検:

- 全 week*.html の外部リンクを curl 一括検証
- NotebookLM・Gemini・Copilot の公式名称・無料枠・UI説明が現状と合うか
- GitHub Education / GitHub Student Pack の特典内容
