# Word変換テンプレート（docx-templates/）

Markdown原稿を Word（.docx）に変換するための参照テンプレート集。日常の作業・記録は Markdown で書き、クライアント共有や社内決裁などで **Word形式が必要になったときだけ変換する** 方針。変換は pandoc + このフォルダの参照テンプレートで行う。

## テンプレート一覧

| ファイル | 用途 | フォーマット |
|---|---|---|
| `簡易版.docx` | クライアント共有・相手が編集する前提の資料 | メイリオ10pt・装飾なし |
| `装飾版.docx` | 提案書・レポート・社内報告 | メイリオ10pt・見出し色付き・引用ボックス |
| `契約書版.docx` | 契約書・合意書・フォーマル文書 | MS明朝10.5pt・MSゴシック見出し |

## 変換手順

### 1. pandocのインストール（初回のみ）

| OS | コマンド |
|---|---|
| Mac | `brew install pandoc` |
| Windows | `winget install --id JohnMacFarlane.Pandoc` または [pandoc.org](https://pandoc.org/installing.html) からインストーラを取得 |

インストール済みかは `pandoc --version` で確認できる。

### 2. 変換コマンド

```bash
pandoc 原稿.md -o 出力.docx --reference-doc=docx-templates/装飾版.docx
```

用途に応じて `--reference-doc=` のテンプレートを切り替える:

```bash
# クライアント共有（装飾なし）
pandoc 原稿.md -o 出力.docx --reference-doc=docx-templates/簡易版.docx

# 提案書・レポート（装飾あり）
pandoc 原稿.md -o 出力.docx --reference-doc=docx-templates/装飾版.docx

# 契約書・フォーマル文書
pandoc 原稿.md -o 出力.docx --reference-doc=docx-templates/契約書版.docx
```

### 3. Claude Codeへの依頼

「これWordにして」「装飾版でdocxにして」などと依頼すれば、Claude Codeが用途を確認して適切なテンプレートを選び、pandoc未インストールならインストール提案から実行する。

## 自社ブランドに合わせて参照テンプレートを差し替える場合

ロゴ・色・フォントを自社スタイルに変更したいときは、同梱のdocxを上書き編集するだけでよい:

1. 対象の参照テンプレート（例: `装飾版.docx`）をWordで開く
2. フォント・色・ヘッダー/フッター・ロゴなどを編集して上書き保存
3. 以降の変換で同じ `--reference-doc=...` を指定すれば自社スタイルで出力される

※ 参照テンプレート内のサンプル文章は「スタイル定義のひな形」として使われるだけで、本文はmdから流し込まれる。サンプル文章自体を削除する必要はない。

## よく使うpandocオプション

| オプション | 用途 |
|---|---|
| `--reference-doc=...` | 参照テンプレートを指定（必須） |
| `--toc` | 目次を自動生成 |
| `--toc-depth=2` | 目次に含める見出しレベル（デフォルト3） |
| `-N` / `--number-sections` | 見出しに章番号を自動付与 |

例: 目次付き・章番号付きの提案書を作る:

```bash
pandoc 原稿.md -o 提案書.docx --reference-doc=docx-templates/装飾版.docx --toc -N
```
