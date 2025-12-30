# Reversi Legal Move Methods Comparison

このリポジトリは、**リバーシ（オセロ）の合法手判定プログラム** を異なる開発アプローチで実装し、比較する実験プロジェクトです。同一の課題に対して複数の開発手法を適用することで、各アプローチの特徴、利点、課題を明確にします。

## 課題

リバーシの盤面と手番を入力として受け取り、合法手の位置に `0` をマークした盤面を出力するプログラムを実装します。

詳細は [`problem/problem_statement.md`](problem/problem_statement.md) を参照してください。

## 共通条件
- 使用言語は Python (3.11.2)
- 出力はコンソール
- 依存関係と実行手順は各アプローチで統一
- 入出力フォーマットは全アプローチで統一
- テストは `pytest` で統一（同一のテストケースを流用できる形にする）

各アプローチは、上記の共通条件と `problem/problem_statement.md` をあわせて読んでください。

## 実装済みアプローチ

### 1. plan_driven アプローチ

**特徴**: 事前の詳細な計画とテスト駆動開発（TDD）を組み合わせた実装方法

**主な要素**:
- **事前設計**: DESIGN.md でアーキテクチャと責任分離を明文化
- **計画管理**: plan.md で実装タスクを細分化し、進捗を追跡
- **TDD/BDD**: Red-Green-Refactor サイクルと日本語テスト名による振る舞い駆動開発
- **レイヤードアーキテクチャ**: domain層（ビジネスロジック）と io層（入出力）を分離

**テスト状況**: 全26テストがパス（Board: 6, GameRules: 11, IO層: 6, E2E: 3）

**詳細**: [`approaches/plan_driven/README.md`](approaches/plan_driven/README.md)

**Git履歴**: 各コミットが TDD サイクルの完了を表し、実装過程が追跡可能

## ディレクトリ構成

```
reversi-legal-move-methods-comparison/
├── problem/
│   └── problem_statement.md    # 課題の詳細
├── approaches/
│   └── plan_driven/             # plan_driven アプローチ
│       ├── domain/              # ドメイン層（ビジネスロジック）
│       ├── io/                  # IO層（入出力処理）
│       ├── tests/               # テストコード
│       ├── reversi.py           # メインエントリポイント
│       ├── DESIGN.md            # 設計書
│       ├── plan.md              # 実装計画と進捗管理
│       └── README.md            # アプローチ詳細
└── README.md                    # このファイル
```

## 今後の予定

他の開発アプローチ（例: アジャイル、プロトタイピング、リファクタリング重視など）を追加し、比較分析を行う予定です。
