# Reversi Legal Move Methods Comparison

このリポジトリは比較実験用のプロジェクトです。同一の課題に対して複数の開発アプローチを適用し、結果を整理します。

## 課題

詳細は `problem/problem_statement.md` を参照してください。

## 共通条件
- 使用言語は Python (3.11.2)
- 出力はコンソール
- 依存関係と実行手順は各アプローチで統一
- 入出力フォーマットは全アプローチで統一
- テストは `pytest` で統一（同一のテストケースを流用できる形にする）

各アプローチは、上記の共通条件と `problem/problem_statement.md` をあわせて読んでください。

## 現在の状況
- 完了: plan_driven / spec_driven / tdd_ai_assisted / vibe_coding

## ドキュメント
- 各アプローチの結果: `docs/reports/`
- 比較レポート: `docs/comparisons/`（`overall_analysis.md`）
- plan_driven の詳細: `docs/approaches/plan_driven.md`

## ディレクトリ構成

```
reversi-legal-move-methods-comparison/
├── problem/
│   └── problem_statement.md
├── approaches/
│   ├── plan_driven/
│   ├── spec_driven/
│   ├── tdd_ai_assisted/
│   └── vibe_coding/
├── docs/
│   ├── approaches/
│   ├── comparisons/
│   └── reports/
└── README.md
```
