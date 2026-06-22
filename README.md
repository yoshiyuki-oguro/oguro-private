# Claude Code Business Template

Claude Codeでビジネス業務を管理するためのテンプレートリポジトリ。

## 使い方

1. 「Use this template」からリポジトリを作成
2. `CLAUDE.md` を自分の情報・業務に合わせて編集
3. `memory/PERSISTENT.md` に担当業務の基本情報を記入
4. `memory/2026-05-01-sample.md` を読んでフォーマットを確認したら削除してOK
5. VS CodeでClaude Code拡張を開いて作業開始

## 構成

```
.
├── CLAUDE.md                        ← AIへの指示書（自分用にカスタマイズ）
├── memory/
│   ├── PERSISTENT.md                ← 長期記憶（確定事項・学び）
│   └── 2026-05-01-sample.md         ← 短期記憶のサンプル（削除OK）
├── docx-templates/                  ← md→Word変換用の参照テンプレート
│   ├── 簡易版.docx                  ← クライアント共有・装飾なし
│   ├── 装飾版.docx                  ← 提案書・レポート
│   └── 契約書版.docx                ← 契約書・フォーマル文書
└── .claude/
    ├── settings.local.json          ← セキュリティ設定（危険な操作をブロック）
    └── skills/
        ├── finish/SKILL.md          ← セッション終了（/finish）
        ├── review-memory/SKILL.md   ← 記憶の棚卸し（/review-memory）
        └── sync-skills/SKILL.md     ← 共有スキルの同期（/sync-skills）
```

### Word変換（pandoc）

Markdownファイルを .docx に変換したいときは、同梱の参照テンプレート + pandocで変換する。詳細な手順・テンプレートの使い分け・自社ブランドへのカスタマイズ方法は [`docx-templates/README.md`](docx-templates/README.md) を参照。

## スキル

| コマンド | 内容 |
|---|---|
| `/finish` | セッション終了時の記憶更新・波及チェック・ファイル整理・ネクストアクション整理・コミット（共有リポジトリの同期含む） |
| `/review-memory` | 記憶ファイルの棚卸し・整理（長期記憶への昇格、古い短期記憶の整理） |
| `/sync-skills` | 共有リポジトリの `スキル共有/` から共有スキルを個人環境にコピー |

## 共有プロジェクトとの連携

チームで共有するドキュメントは別のGitリポジトリ（共有テンプレート: `claude-code-shared-template`）で管理する。

- Claude Codeはこの個人プロジェクトから起動し、共有リポジトリのファイルを読み書きする
- 共有リポジトリのパスをCLAUDE.mdに設定しておけば、git pull/push・コンフリクト解消をClaude Codeが自動で行う
- 記憶（memory/）は個人プロジェクトのみ。共有リポジトリには置かない
- 共有スキルは `/sync-skills` で個人環境に同期する

## セキュリティ

`.claude/settings.local.json` に以下のデフォルト設定が入っています:

- `rm -rf` / `rm -r` の実行を禁止（ファイルの一括削除を防止）
