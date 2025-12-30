# plan_driven アプローチ

## 概要

plan_driven アプローチは、**事前の詳細な計画とテスト駆動開発（TDD）** を組み合わせた実装方法です。このアプローチでは、コードを書く前に設計書と計画書を作成し、Red-Green-Refactor サイクルに従って段階的に実装を進めます。

## アプローチの特徴

### 1. 事前の詳細な設計
- **DESIGN.md**: アーキテクチャ、クラス設計、責任分離を明文化
- **plan.md**: 実装タスクを細分化し、各タスクの目的と完了定義を記述
- **レイヤードアーキテクチャ**: domain層（ビジネスロジック）と io層（入出力）を分離

### 2. テスト駆動開発（TDD）の実践
- **Red-Green-Refactor サイクル**:
  1. **Red**: 失敗するテストを先に書く
  2. **Green**: テストをパスする最小限の実装
  3. **Refactor**: コードの品質向上とコミット
- **各サイクルでコミット**: Git履歴でTDDの進行が追跡可能

### 3. 振る舞い駆動開発（BDD）の実践
- **日本語テスト名**: テストが振る舞いを表現（例: `test_盤面を初期化できる()`）
- **Given-When-Then 構造**: テストケースが仕様書として機能
- **内側と外側のループ**:
  - 内側: ユニットテスト（Board, GameRules, InputReader, OutputWriter）
  - 外側: エンドツーエンドテスト（reversi.py の統合テスト）

### 4. 進捗管理
- **plan.md での進捗追跡**: 各タスクの状態（⏳ 未着手、🔄 実施中、✅ 完了）を記録
- **コミット番号の記録**: 各タスク完了時のコミットを plan.md に記録

## ディレクトリ構成

```
approaches/plan_driven/
├── domain/                  # ドメイン層（ビジネスロジック）
│   ├── __init__.py
│   ├── board.py            # Board クラス（盤面管理）
│   └── game_rules.py       # GameRules クラス（合法手判定）
├── io/                     # IO層（入出力処理）
│   ├── __init__.py
│   ├── input_reader.py     # InputReader クラス（標準入力）
│   └── output_writer.py    # OutputWriter クラス（標準出力）
├── tests/                  # テストコード
│   ├── __init__.py
│   ├── test_board.py       # Board のユニットテスト
│   ├── test_game_rules.py  # GameRules のユニットテスト
│   ├── test_input_reader.py # InputReader のユニットテスト
│   ├── test_output_writer.py # OutputWriter のユニットテスト
│   └── test_reversi.py     # エンドツーエンドテスト
├── reversi.py              # メインエントリポイント
├── requirements.txt        # pytest>=7.0.0
├── DESIGN.md               # 設計書
├── plan.md                 # 実装計画と進捗管理
└── README.md               # このファイル
```

## セットアップ

```bash
cd approaches/plan_driven

# 依存関係のインストール
pip install -r requirements.txt
```

## 実行方法

```bash
# 標準入力から盤面と手番を受け取り、合法手を出力
python reversi.py < input.txt

# または echo を使用
echo "........
........
........
...WB...
...BW...
........
........
........
B" | python reversi.py
```

### 入力フォーマット
- 8行: 盤面データ（各行8文字、`.` 空マス、`B` 黒、`W` 白）
- 1行: 手番（`B` または `W`）

### 出力フォーマット
- 8行: 盤面データ（合法手の位置に `0` をマーク）
- 1行: 手番

## テスト実行

```bash
# 全テスト実行
pytest tests/ -v

# 特定のテストファイル実行
pytest tests/test_board.py -v

# 特定のテスト実行
pytest tests/test_board.py::test_盤面を初期化できる -v
```

## 実装の過程

### フェーズ0: 準備
1. ブランチ作成 (`feature/plan-driven`)
2. ディレクトリ構造作成
3. DESIGN.md と plan.md 作成

### フェーズ1: Board クラス（TDD サイクル）
1. **Red**: Board クラスのテストを書く（6テスト）
2. **Green**: Board クラスを実装
3. **Refactor**: リファクタリングとコミット

### フェーズ2: GameRules クラス（TDD サイクル × 3回）
#### サイクル1: 方向別ひっくり返し判定
1. **Red**: `can_flip_in_direction` のテストを書く（5テスト）
2. **Green**: メソッドを実装
3. **Refactor**: リファクタリングとコミット

#### サイクル2: 合法手判定
1. **Red**: `is_legal_move` のテストを書く（3テスト）
2. **Green**: メソッドを実装
3. **Refactor**: リファクタリングとコミット

#### サイクル3: 全合法手列挙
1. **Red**: `find_all_legal_moves` のテストを書く（3テスト）
2. **Green**: メソッドを実装
3. **Refactor**: リファクタリングとコミット

### フェーズ3: IO層（TDD サイクル × 2回）
#### サイクル1: InputReader
1. **Red**: InputReader のテストを書く（3テスト）
2. **Green**: InputReader を実装
3. **Refactor**: リファクタリングとコミット

#### サイクル2: OutputWriter
1. **Red**: OutputWriter のテストを書く（3テスト）
2. **Green**: OutputWriter を実装
3. **Refactor**: リファクタリングとコミット

### フェーズ4: 統合（BDD - 外側のループ）
1. **Red**: エンドツーエンドテストを書く（3テスト）
2. **Green**: reversi.py を実装
3. **Refactor**: リファクタリングとコミット
4. 手動テスト実行（黒番・白番）

### フェーズ5: ドキュメント化
1. README.md 作成
2. プロジェクトルート README.md 更新

## テスト状況

**全26テストがパス**:
- Board: 6テスト
- GameRules: 11テスト
- InputReader: 3テスト
- OutputWriter: 3テスト
- reversi.py（E2E）: 3テスト

## Git コミット履歴

```
fcd5c9d docs(plan): タスク4-4 完了を記録
e528afa docs(plan): 進捗を更新
5a9863b feat: メインエントリポイント reversi.py を実装
ad136e5 feat(io): OutputWriter を実装
6971c0f feat(io): InputReader を実装
a8b57a5 feat(domain): GameRules の全合法手列挙を実装
fc2f439 feat(domain): GameRules の合法手判定を実装
4c8bf46 feat(domain): GameRules の方向別ひっくり返し判定を実装
c3d8654 feat(domain): Board クラスを TDD で実装
b0b5faf feat(setup): plan_driven アプローチの初期セットアップ
```

各コミットが TDD サイクルの完了を表しています。

## 設計の特徴

### クラス設計

#### Board クラス（domain/board.py）
**責任**: 盤面の状態管理と基本操作

**主要メソッド**:
- `__init__(grid)`: 盤面初期化
- `get_cell(row, col)`: セル取得
- `is_valid_position(row, col)`: 位置の妥当性チェック
- `is_empty(row, col)`: 空マスチェック
- `to_grid()`: 盤面データ取得
- `get_opponent(player)`: 相手プレイヤー取得（静的メソッド）

#### GameRules クラス（domain/game_rules.py）
**責任**: 合法手判定ロジック

**主要メソッド**:
- `can_flip_in_direction(row, col, dr, dc, player)`: 方向別ひっくり返し判定
- `is_legal_move(row, col, player)`: 1マスの合法性判定
- `find_all_legal_moves(player)`: 全合法手の列挙

**アルゴリズム**:
1. 8方向のベクトルを定義
2. 各方向に対して、相手のコマを挟めるかチェック
3. 挟める方向が1つでもあれば合法手

#### InputReader クラス（io/input_reader.py）
**責任**: 標準入力からの読み込み

**主要メソッド**:
- `read_from_stdin()`: 盤面と手番を読み込み、Board オブジェクトと手番を返す

#### OutputWriter クラス（io/output_writer.py）
**責任**: 標準出力への書き込み

**主要メソッド**:
- `write_board_with_legal_moves(board, legal_moves, player)`: 合法手をマークして出力

### データフロー

```
標準入力
  ↓
InputReader (盤面と手番を読み込み)
  ↓
Board オブジェクト生成
  ↓
GameRules (合法手を計算)
  ↓
合法手リスト
  ↓
OutputWriter (合法手をマークして出力)
  ↓
標準出力
```

## 学んだこと

### TDD/BDD の実践
1. **テストファーストの効果**: テストを先に書くことで、インターフェースが明確になり、実装がシンプルになった
2. **日本語テスト名の価値**: テストが仕様書として機能し、コードレビューが容易になった
3. **小さいサイクルの重要性**: 各メソッドごとに Red-Green-Refactor を回すことで、バグの混入を防げた

### 設計の重要性
1. **事前設計の価値**: DESIGN.md で責任を明確化することで、実装がスムーズになった
2. **レイヤードアーキテクチャ**: domain層と io層を分離することで、テストが容易になった
3. **計画の効果**: plan.md でタスクを細分化することで、進捗が可視化され、モチベーション維持に繋がった

### 技術的な学び
1. **Python の標準ライブラリとの競合**: `io` パッケージ名が標準ライブラリと競合し、`importlib` を使った手動インポートが必要だった
2. **pytest の活用**: `capsys` fixture を使った標準出力のキャプチャ、`unittest.mock.patch` を使った標準入力のモック
3. **型ヒントの効果**: 型ヒントを完備することで、IDEの補完が効き、バグの早期発見に繋がった

## まとめ

plan_driven アプローチは、**事前の詳細な計画とTDD/BDDの組み合わせ** により、高品質なコードを段階的に構築できる方法です。特に、以下の点で有効でした:

- **明確な設計**: DESIGN.md と plan.md により、実装の方向性が明確
- **テストによる品質保証**: 26テスト全てがパスし、エンドツーエンドで動作確認
- **Git履歴での追跡**: 各コミットが TDD サイクルの完了を表し、実装過程が明確
- **進捗の可視化**: plan.md でタスクの状態を管理し、進捗が一目瞭然

このアプローチは、要件が明確で、設計を事前に固められるプロジェクトに適しています。
