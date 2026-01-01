# TDD AI-Assisted アプローチ

リバーシ（オセロ）の合法手判定プログラムを**テスト駆動開発（TDD）とAIアシスタント**で実装したプロジェクトです。

## 概要

このプロジェクトでは、AIアシスタント（Claude）と協力しながら、ケント・ベックのTDD手法に従って段階的に実装を進めました。8方向すべての合法手を判定し、コマンドラインから実行可能な完全なプログラムとして完成しています。

## 機能

- ✅ リバーシの盤面状態を表現
- ✅ 8方向すべての合法手を計算
- ✅ 標準入力からボードと手番を読み込み
- ✅ 標準出力に合法手を表示
- ✅ Value Object パターンによる型安全性
- ✅ 責任の明確な分離（SRP原則）

## 使い方

### 基本的な使用方法

```bash
# 標準入力から実行
cat input.txt | python main.py

# または
python main.py < input.txt
```

### 入力フォーマット

```
........
........
........
...BW...
...WB...
........
........
........
B
```

- 最後の行が手番（B または W）
- それ以外がボードの状態
  - `B`: 黒石
  - `W`: 白石
  - `.`: 空きマス

### 出力フォーマット

```
........
........
....0...
...BW0..
..0WB...
...0....
........
........
B
```

- `0`: 合法手の位置
- 最後の行に手番を表示

## セットアップ

### 前提条件
- Python 3.11.2 以上

### インストール手順

```bash
cd approaches/tdd_ai_assisted
pip install -r requirements.txt
```

## テスト実行

```bash
# 全テスト実行
pytest -v

# 特定のテストファイル実行
pytest test_board.py -v
pytest test_main.py -v
```

**テスト状況：20テスト、すべて通過 ✅**

## ファイル構成

```
tdd_ai_assisted/
├── board.py                    # Board クラス（Value Object）、Stone Enum
├── legal_move_calculator.py    # LegalMoveCalculator クラス
├── main.py                     # コマンドラインインターフェース
├── test_board.py              # Board のテスト（18テスト）
├── test_main.py               # main のテスト（2テスト）
├── TODO.md                    # 実装計画（完了）
├── requirements.txt           # 依存関係
└── README.md                  # このファイル
```

## 設計

### アーキテクチャ

**Value Object パターン**
- `Board`: 盤面の状態を表す不変オブジェクト
  - バリデーション機能を持つ
  - 型安全性を提供
  - 読み取り専用プロパティ

**責任の分離（SRP原則）**
- `Board`: 盤面の状態を表現
- `LegalMoveCalculator`: 合法手の計算ロジック
- `main`: 標準入力/出力のインターフェース

**依存関係**
```
main.py
  ├─→ board.py (Board, Stone)
  └─→ legal_move_calculator.py
        └─→ board.py (Board, Stone)
```

### クラス設計

**Board クラス**
```python
class Board:
    EMPTY = "."
    VALID_CHARS = frozenset({...})

    def __init__(self, board: str)
    @property board(self) -> str
    @staticmethod string_to_array(board_str: str) -> list[list[str]]
    @staticmethod array_to_string(board: list[list[str]]) -> str
```

**LegalMoveCalculator クラス**
```python
class LegalMoveCalculator:
    LEGAL_MOVE_MARK = "0"

    @staticmethod calculate(board: Board, turn: Stone) -> str
```

## 実装の経緯

### TDD プロセス

このプロジェクトは、**Red-Green-Refactor サイクル**を厳密に実践して実装されました。

**1. 最小のテストから開始**
- 1x1のボード
- ボードの生成と表示

**2. 段階的な機能追加**
- 3x1のボード（横方向の合法手）
- 1x3のボード（縦方向の合法手）
- 3x3のボード（斜め方向の合法手）
- 8x8のボード（実際のリバーシ）

**3. 方向チェックの実装**
- 左方向 → 上方向 → 左上方向
- DRY原則に基づくリファクタリング
- 方向ベクトル `(dx, dy)` の導入
- 8方向すべての実装

**4. 設計の改善**
- メタファーの見直し（Board と LegalMoveCalculator の分離）
- Value Object パターンの適用
- ファイル分割（関心の分離）

**5. コマンドラインインターフェース**
- main.py の追加
- 標準入力/出力のサポート

### リファクタリングの履歴

1. **メソッド名の改善**
   - `limit_move` → `with_legal_moves`

2. **DRY原則の適用**
   - マジックストリング → 定数化
   - 繰り返しロジック → ヘルパーメソッド

3. **責任の分離**
   - `Board` と `LegalMoveCalculator` の分離
   - 手番を `Board` から分離

4. **ファイル分割**
   - `LegalMoveCalculator` を別ファイルに

5. **Value Object パターン**
   - `Board` を不変オブジェクトとして設計
   - 読み取り専用プロパティの追加

## 学んだこと

### TDDの実践
- ✅ 最小のステップで進めることの重要性
- ✅ テストファーストのメリット
- ✅ Red-Green-Refactorのリズム
- ✅ 具体から抽象への進化

### 設計原則
- ✅ SOLID原則（特にSRP）
- ✅ DRY原則
- ✅ YAGNI原則
- ✅ Value Object パターン

### AIアシスタントとの協力
- ✅ 効率的なペアプログラミング
- ✅ 設計の議論とフィードバック
- ✅ リファクタリングの提案
- ✅ TDD原則の理解を深める

## まとめ

TDD AI-Assistedアプローチは、**純粋なTDD手法とAIアシスタントの協力**により、高品質なコードを段階的に構築する方法です。

**特に有効な点：**
- ✅ TDDの基本原則を実践的に学べる
- ✅ 最小のステップで確実に進める
- ✅ AIとの協力で効率的に開発
- ✅ 設計原則を実践的に適用
- ✅ テストリストで進捗が明確
- ✅ リファクタリングを継続的に実施

**完成した成果物：**
- 20テストすべてパス
- 8方向の合法手判定を完全実装
- クリーンな設計（Value Object、SRP）
- コマンドラインから実行可能
- 保守性の高いコードベース
