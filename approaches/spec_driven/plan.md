# リバーシ合法手判定プログラム - 技術計画書

## 1. 概要

この技術計画書は、`spec.md`で定義した仕様（What/Why）を実現するための具体的な実装戦略（How）を明文化します。

**spec.md との関係**:
- **spec.md**: 何を実現するか（What）、なぜ必要か（Why）
- **plan.md**: どのように実装するか（How）

本ドキュメントでは、アーキテクチャ設計、クラス設計、データフロー、ファイル構成、実装戦略を定義します。

## 2. アーキテクチャ設計

### 2.1 レイヤードアーキテクチャの採用

本プログラムは、**レイヤードアーキテクチャ**を採用し、責任を明確に分離します。

```
┌─────────────────────────────────────┐
│     reversi.py (Entry Point)        │  ← メインエントリポイント
└─────────────────────────────────────┘
           ↓              ↓
┌──────────────────┐  ┌──────────────────┐
│   IO層           │  │  Domain層         │
│  - InputReader   │  │  - Board          │  ← ビジネスロジック
│  - OutputWriter  │  │  - GameRules      │
└──────────────────┘  └──────────────────┘
```

### 2.2 各層の責任

#### Domain層（ドメイン層）
**責任**: ビジネスロジックの実装
- **Board クラス**: 盤面の状態管理
- **GameRules クラス**: リバーシのルールに基づく合法手判定

**特徴**:
- 入出力処理に依存しない（純粋なロジック）
- ユニットテストが容易
- 再利用可能（将来のGUI版などで流用可能）

#### IO層（入出力層）
**責任**: 標準入出力の処理
- **InputReader クラス**: 標準入力からの読み込み
- **OutputWriter クラス**: 標準出力への書き込み

**特徴**:
- Domain層を利用する
- 入出力の詳細をカプセル化

#### Entry Point（エントリポイント）
**責任**: プログラムの実行フロー制御
- `reversi.py`: 各層を統合し、全体のフローを制御

### 2.3 依存関係

```
Entry Point → IO層 → Domain層
```

- **Domain層は他の層に依存しない**（依存関係の逆転）
- IO層はDomain層を使用する
- Entry PointはIO層とDomain層を使用する

## 3. クラス設計

### 3.1 Board クラス（domain/board.py）

#### 責任
- 盤面の状態を管理する
- セルへのアクセスを提供する
- 盤面に関する基本的な操作を提供する
- **ゲームロジックは含まない**（単一責任の原則）

#### クラス定数
```python
EMPTY: str = '.'    # 空マス
BLACK: str = 'B'    # 黒のコマ
WHITE: str = 'W'    # 白のコマ
SIZE: int = 8       # 盤面のサイズ
```

#### メソッド設計

| メソッド名 | 引数 | 戻り値 | 説明 |
|-----------|-----|--------|------|
| `__init__` | `grid: List[List[str]]` | なし | 盤面を初期化する |
| `get_cell` | `row: int, col: int` | `str` | 指定位置のセルの値を取得 |
| `is_valid_position` | `row: int, col: int` | `bool` | 指定位置が盤面内かチェック |
| `is_empty` | `row: int, col: int` | `bool` | 指定位置が空マスかチェック |
| `to_grid` | なし | `List[List[str]]` | 盤面データを取得（コピー） |
| `get_opponent` | `player: str` | `str` | 相手プレイヤーを取得（静的メソッド） |

#### データ構造
```python
class Board:
    def __init__(self, grid: List[List[str]]):
        self._grid: List[List[str]] = grid  # 8x8の盤面（内部状態）
```

#### 設計判断
- **イミュータブル性**: `to_grid()`はコピーを返すことで、外部からの不正な変更を防ぐ
- **静的メソッド**: `get_opponent()`は盤面の状態に依存しないため、静的メソッドとして定義

### 3.2 GameRules クラス（domain/game_rules.py）

#### 責任
- リバーシのゲームルールを実装する
- 合法手の判定を行う
- 全合法手の列挙を行う
- **盤面の状態は変更しない**（副作用を避ける）

#### クラス定数
```python
DIRECTIONS: List[Tuple[int, int]] = [
    (-1, -1), (-1, 0), (-1, 1),  # 上方向3つ
    (0, -1),           (0, 1),    # 左右
    (1, -1),  (1, 0),  (1, 1)     # 下方向3つ
]
```

#### メソッド設計

| メソッド名 | 引数 | 戻り値 | 説明 |
|-----------|-----|--------|------|
| `__init__` | `board: Board` | なし | GameRules を初期化 |
| `can_flip_in_direction` | `row: int, col: int, dr: int, dc: int, player: str` | `bool` | 特定の方向にひっくり返せるかチェック |
| `is_legal_move` | `row: int, col: int, player: str` | `bool` | 指定位置が合法手かチェック |
| `find_all_legal_moves` | `player: str` | `List[Tuple[int, int]]` | 全合法手を列挙 |

#### アルゴリズム詳細

**can_flip_in_direction の判定ロジック**:

1. 隣接マス `(row+dr, col+dc)` が盤面内かチェック
2. 隣接マスに相手のコマがあるかチェック → なければ False
3. その方向に進み続ける:
   - 空マス `.`: False（ひっくり返せない）
   - 自分のコマ: True（ひっくり返せる）
   - 相手のコマ: さらに進む
   - 盤面外: False

```
例: 黒番で (2,4) に置く場合の下方向チェック

    0 1 2 3 4 5 6 7
  ┌─────────────────
0 │ . . . . . . . .
1 │ . . . . . . . .
2 │ . . . . ? . . .  ← ここに置く
3 │ . . . B W . . .
4 │ . . . W B . . .  ← (3,4)=W, (4,4)=B
5 │ . . . . . . . .
  ...

方向: dr=1, dc=0（下方向）

ステップ1: (2+1, 4+0) = (3,4) → 'W'（相手のコマ）✓
ステップ2: (3+1, 4+0) = (4,4) → 'B'（自分のコマ）✓
→ True（ひっくり返せる）
```

**is_legal_move の判定ロジック**:

1. 指定位置が空マスかチェック → 空でなければ False
2. 8方向それぞれについて `can_flip_in_direction` を呼び出す
3. 1方向でもTrueなら合法手

**find_all_legal_moves の判定ロジック**:

1. 盤面の全マス（8×8 = 64マス）をループ
2. 各マスについて `is_legal_move` を呼び出す
3. 合法手であれば `(row, col)` をリストに追加
4. リストを返す

#### データ構造
```python
class GameRules:
    def __init__(self, board: Board):
        self._board: Board = board  # Boardオブジェクトへの参照
```

#### 設計判断
- **8方向の定数化**: DIRECTIONS を定数として定義し、コードの可読性を向上
- **メソッドの分離**: `can_flip_in_direction` → `is_legal_move` → `find_all_legal_moves` と段階的に構築

### 3.3 InputReader クラス（io/input_reader.py）

#### 責任
- 標準入力から盤面と手番を読み込む
- 入力データをパースしてBoard オブジェクトに変換する

#### メソッド設計

| メソッド名 | 引数 | 戻り値 | 説明 |
|-----------|-----|--------|------|
| `read_from_stdin` | なし | `Tuple[Board, str]` | 標準入力から盤面と手番を読み込む（静的メソッド） |

#### 処理フロー
1. 標準入力から9行読み込み
2. 最初の8行を盤面データとして解析（各行を文字のリストに変換）
3. 9行目を手番として解析（空白を除去）
4. Boardオブジェクトを生成
5. `(Board, 手番)` のタプルを返す

#### 実装例
```python
@staticmethod
def read_from_stdin() -> Tuple[Board, str]:
    """標準入力から盤面と手番を読み込む"""
    lines = [input().strip() for _ in range(9)]

    # 最初の8行が盤面
    grid = [list(line) for line in lines[:8]]

    # 9行目が手番
    player = lines[8].strip()

    board = Board(grid)
    return board, player
```

### 3.4 OutputWriter クラス（io/output_writer.py）

#### 責任
- 盤面と合法手を標準出力に書き込む
- 合法手の位置に '0' をマークする

#### メソッド設計

| メソッド名 | 引数 | 戻り値 | 説明 |
|-----------|-----|--------|------|
| `write_board_with_legal_moves` | `board: Board, legal_moves: List[Tuple[int, int]], player: str` | `None` | 合法手をマークして出力（静的メソッド） |

#### 処理フロー
1. 盤面をコピー（元の盤面を変更しないため）
2. 合法手の位置に '0' をマーク
3. 8行の盤面を出力
4. 手番を出力

#### 実装例
```python
@staticmethod
def write_board_with_legal_moves(
    board: Board,
    legal_moves: List[Tuple[int, int]],
    player: str
) -> None:
    """合法手をマークした盤面を出力する"""
    # 盤面をコピー
    grid = board.to_grid()

    # 合法手の位置に '0' をマーク
    for row, col in legal_moves:
        grid[row][col] = '0'

    # 盤面を出力
    for row in grid:
        print(''.join(row))

    # 手番を出力
    print(player)
```

## 4. データフロー

### 4.1 全体のデータフロー

```
[ 標準入力 ]
     ↓
[ InputReader.read_from_stdin() ]
     ↓
(Board, player: str)
     ↓
[ GameRules(board).find_all_legal_moves(player) ]
     ↓
legal_moves: List[Tuple[int, int]]
     ↓
[ OutputWriter.write_board_with_legal_moves(board, legal_moves, player) ]
     ↓
[ 標準出力 ]
```

### 4.2 詳細なデータフロー

1. **入力処理**
   - 標準入力から9行のテキストを読み込む
   - InputReader が盤面データ（8行）と手番データ（1行）を分離
   - 盤面データを `List[List[str]]` に変換
   - Board オブジェクトを生成

2. **合法手判定処理**
   - GameRules オブジェクトを生成（Board を渡す）
   - `find_all_legal_moves(player)` を呼び出す
   - 盤面の全マス（64マス）について合法手判定
   - 合法手の座標リスト `List[Tuple[int, int]]` を取得

3. **出力処理**
   - 盤面をコピー
   - 合法手の位置に '0' をマーク
   - 8行の盤面データを標準出力
   - 手番を標準出力

### 4.3 データの不変性

- **Board**: 一度生成されたら内部状態は変更されない
- **GameRules**: 盤面の状態を変更しない（読み取り専用）
- **OutputWriter**: 元の Board を変更せず、コピーに対して '0' をマーク

## 5. ファイル構成

### 5.1 ディレクトリ構造

```
approaches/spec_driven/
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
├── spec.md                 # 仕様書（What/Why）
├── plan.md                 # 技術計画書（How）← このファイル
└── README.md               # アプローチ説明
```

### 5.2 各ファイルの役割

| ファイル | 役割 | 依存関係 |
|---------|------|---------|
| `domain/board.py` | 盤面の状態管理 | なし（純粋なロジック） |
| `domain/game_rules.py` | 合法手判定ロジック | `domain/board.py` |
| `io/input_reader.py` | 標準入力からの読み込み | `domain/board.py` |
| `io/output_writer.py` | 標準出力への書き込み | `domain/board.py` |
| `reversi.py` | メインエントリポイント | 全モジュール |
| `tests/*.py` | テストコード | 対応するモジュール |
| `requirements.txt` | 依存パッケージ | - |

## 6. 入出力仕様の技術的詳細

### 6.1 入力形式のパース

**入力フォーマット**:
```
........    ← 盤面1行目（8文字）
........    ← 盤面2行目
........    ← 盤面3行目
...BW...    ← 盤面4行目
...WB...    ← 盤面5行目
........    ← 盤面6行目
........    ← 盤面7行目
........    ← 盤面8行目
B           ← 手番（'B' または 'W'）
```

**パース処理**:
1. `input()` で9行読み込む
2. 各行に対して `.strip()` で前後の空白を除去
3. 最初の8行を `list()` で文字のリストに変換
4. 9行目を手番として保存

**データ構造**:
- 盤面: `List[List[str]]` (8×8の2次元リスト)
- 手番: `str` ('B' または 'W')

### 6.2 出力形式の生成

**出力フォーマット**:
```
........    ← 盤面1行目
........    ← 盤面2行目
....0...    ← 盤面3行目（合法手を '0' で表示）
...BW0..    ← 盤面4行目
..0WB...    ← 盤面5行目
...0....    ← 盤面6行目
........    ← 盤面7行目
........    ← 盤面8行目
B           ← 手番
```

**生成処理**:
1. `board.to_grid()` で盤面をコピー
2. 合法手の座標リストをループ
3. 各座標 `(row, col)` に対して `grid[row][col] = '0'` を設定
4. 各行を `''.join(row)` で文字列に変換して出力
5. 手番を出力

## 7. 実装戦略

### 7.1 実装の優先順位

実装は以下の順序で行います：

1. **Board クラス** → 基盤となるデータ構造
2. **Board のテスト** → Board の正しさを保証
3. **GameRules クラス** → コアロジック
4. **GameRules のテスト** → ロジックの正しさを保証
5. **InputReader クラス** → 入力処理
6. **InputReader のテスト** → 入力処理の正しさを保証
7. **OutputWriter クラス** → 出力処理
8. **OutputWriter のテスト** → 出力処理の正しさを保証
9. **reversi.py** → 統合
10. **統合テスト** → 全体の動作確認

### 7.2 テスト戦略

#### ユニットテスト

**tests/test_board.py**:
- Board クラスの各メソッドをテスト
- 境界値テスト（盤面外のアクセス）
- 空マスチェック
- `get_opponent` の正しさ

**tests/test_game_rules.py**:
- `can_flip_in_direction` の各方向テスト
- `is_legal_move` の各パターンテスト
- `find_all_legal_moves` の初期配置テスト

**tests/test_input_reader.py**:
- 標準入力からの読み込みテスト（モックを使用）
- Board オブジェクトへの変換テスト

**tests/test_output_writer.py**:
- 合法手マーキングのテスト
- 標準出力のテスト（モックを使用）

#### 統合テスト

**tests/test_reversi.py**:
- エンドツーエンドのテスト
- spec.md の受入基準（AC-001〜AC-006）を満たすことを確認
- 初期配置（黒番、白番）
- 合法手がない場合
- エッジケース

### 7.3 技術スタック

| 項目 | 技術 | バージョン |
|------|------|----------|
| 言語 | Python | 3.x |
| テストフレームワーク | pytest | >= 7.0.0 |
| 型チェック | 型ヒント（typing） | 標準ライブラリ |
| ドキュメント | docstring（日本語） | - |

### 7.4 段階的な実装アプローチ

**フェーズ1: 基盤構築**
1. ディレクトリ構造作成
2. `requirements.txt` 作成
3. Board クラスとテスト実装

**フェーズ2: コアロジック**
1. GameRules クラス実装
2. ユニットテスト実装

**フェーズ3: IO層**
1. InputReader クラス実装
2. OutputWriter クラス実装
3. ユニットテスト実装

**フェーズ4: 統合**
1. `reversi.py` 実装
2. 統合テスト実装
3. 手動テスト実行

**フェーズ5: ドキュメント化**
1. README.md 作成
2. コードレビュー

## 8. 技術的な設計判断

### 8.1 なぜレイヤードアーキテクチャか

**理由**:
- **責任の明確化**: domain層とio層を分離することで、各層の責任が明確になる
- **テストしやすさ**: domain層は入出力に依存しないため、ユニットテストが容易
- **拡張性**: 将来、GUI版やWeb版を作る際、domain層を再利用できる
- **保守性**: 各層が独立しているため、変更の影響範囲が限定される

### 8.2 なぜクラスベースか

**理由**:
- **状態のカプセル化**: Board は盤面の状態を持つため、クラスが適切
- **メソッドのグループ化**: 関連するメソッドをまとめることで可読性向上
- **単一責任の原則**: 各クラスが1つの責任のみを持つ
- **オブジェクト指向の利点**: 継承や多態性を活用できる（将来の拡張）

### 8.3 なぜBoard とGameRules を分離するか

**理由**:
- **Board**: 「盤面の状態管理」という責任
- **GameRules**: 「ゲームルールの判定」という責任
- 分離することで、それぞれが独立してテスト可能になる
- リバーシ以外のゲームでも Board を再利用できる可能性

### 8.4 なぜ静的メソッドを使うか

**理由**:
- **InputReader** と **OutputWriter** は状態を持たない
- 静的メソッドにすることで、インスタンス生成のオーバーヘッドを削減
- 関数として定義することもできるが、クラスにまとめることで名前空間を整理

### 8.5 拡張性への配慮

**将来の拡張に対応しやすい設計**:

1. **可変サイズの盤面**:
   - Board.SIZE を定数として定義
   - 将来、コンストラクタで size を受け取るように拡張可能

2. **GUI版への対応**:
   - domain層は入出力に依存しないため、そのまま再利用可能
   - IO層のみを GUI 用に置き換える

3. **AI対戦への対応**:
   - GameRules を拡張して、最適手を選択するAIを実装可能

4. **他のゲームへの応用**:
   - Board クラスは汎用的なため、チェスや将棋などにも応用可能

## 9. 仕様との対応

### 9.1 spec.md の受入基準との対応

| 受入基準 | 対応する実装 |
|---------|-------------|
| **AC-001**: 初期配置での黒番の合法手判定 | `GameRules.find_all_legal_moves('B')` |
| **AC-002**: 初期配置での白番の合法手判定 | `GameRules.find_all_legal_moves('W')` |
| **AC-003**: 合法手がない場合 | `find_all_legal_moves` が空リストを返す |
| **AC-004**: 複数方向にひっくり返せる場合 | `can_flip_in_direction` の8方向チェック |
| **AC-005**: 端や角での合法手判定 | `Board.is_valid_position` で境界チェック |
| **AC-006**: 入出力の正確性 | `InputReader`, `OutputWriter` の実装 |

### 9.2 機能要件との対応

| 機能要件 | 対応する実装 |
|---------|-------------|
| **FR-001**: 入力仕様 | `InputReader.read_from_stdin()` |
| **FR-002**: 出力仕様 | `OutputWriter.write_board_with_legal_moves()` |
| **FR-003**: 合法手の定義 | `GameRules.is_legal_move()` |
| **FR-004**: 全方向の判定 | `GameRules.DIRECTIONS` と8方向ループ |

### 9.3 非機能要件との対応

| 非機能要件 | 対応する設計 |
|-----------|-------------|
| **NFR-001**: 正確性 | ユニットテスト・統合テストで保証 |
| **NFR-002**: 使いやすさ | 標準入出力を使用、シンプルなインターフェース |
| **NFR-003**: 拡張性 | レイヤードアーキテクチャ、責任分離 |

## 10. まとめ

本技術計画書に基づいて実装を進めることで、以下を実現します：

1. **明確な責任分離**: 各クラスが単一責任を持つ
2. **高いテスタビリティ**: ユニットテスト・統合テストが容易
3. **高い保守性**: コードの意図が明確で、変更が容易
4. **高い拡張性**: 将来の機能追加に対応しやすい
5. **spec.md との整合性**: 全ての受入基準と機能要件を満たす

この技術計画書を実装の指針として、段階的に開発を進めます。
