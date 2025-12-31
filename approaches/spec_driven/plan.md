# リバーシ合法手判定プログラム - 技術計画書

## 1. 概要

この技術計画書は、`spec.md`で定義した仕様を実現するための具体的な実装方針を定義します。

**spec.md との関係**:
- **spec.md**: 何を実現するか（What）、なぜ必要か（Why）
- **plan.md**: どのように実装するか（How）

## 2. 技術的アプローチ

### 2.1 基本方針

spec.mdの要件を満たすために、以下の方針で実装します：

1. **シンプルな実装**: 過度な抽象化を避け、要件を満たす最小限の構造
2. **テスト可能性**: spec.mdの受入基準をテストコードで検証
3. **標準入出力の活用**: Pythonの標準機能のみで実装

### 2.2 プログラム構造

```
reversi.py (メインプログラム)
├── 盤面データ構造（8x8の2次元リスト）
├── 合法手判定関数
└── 入出力処理
```

単一ファイルでの実装も可能ですが、保守性とテスト容易性を考慮して、以下のように機能を分割します：

- **reversi_core.py**: 合法手判定の核となるロジック
- **reversi.py**: メインエントリポイント（入出力と統合）
- **test_reversi.py**: テストコード

## 3. データ構造

### 3.1 盤面の表現

盤面は `List[List[str]]` で表現します：

```python
# 8x8の2次元リスト
grid: List[List[str]] = [
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', 'W', 'B', '.', '.', '.'],
    ['.', '.', '.', 'B', 'W', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.']
]
```

**文字の意味**:
- `'.'`: 空マス
- `'B'`: 黒のコマ
- `'W'`: 白のコマ

### 3.2 座標の表現

座標は `(row, col)` のタプルで表現します：
- `row`: 行番号（0〜7）
- `col`: 列番号（0〜7）

### 3.3 合法手のリスト

合法手は `List[Tuple[int, int]]` で表現します：

```python
legal_moves = [(2, 4), (3, 5), (4, 2), (5, 3)]  # 初期配置・黒番の例
```

## 4. 主要な関数設計

### 4.1 合法手判定の核となる関数

#### `can_place_and_flip(grid, row, col, player) -> bool`

指定された位置にコマを置くことができ、少なくとも1つ以上の相手のコマをひっくり返せるかを判定します。

**引数**:
- `grid`: 盤面データ
- `row`, `col`: 置く位置
- `player`: 現在のプレイヤー（'B' または 'W'）

**戻り値**: `bool` - 合法手ならTrue

**ロジック**:
1. 指定位置が空マスでなければ False
2. 8方向（上下左右、斜め）それぞれについて：
   - その方向に相手のコマが連続し、その先に自分のコマがあるかチェック
3. 1方向でもひっくり返せればTrue、すべて不可ならFalse

#### `find_legal_moves(grid, player) -> List[Tuple[int, int]]`

すべての合法手を見つけます。

**引数**:
- `grid`: 盤面データ
- `player`: 現在のプレイヤー

**戻り値**: `List[Tuple[int, int]]` - 合法手の座標リスト

**ロジック**:
1. 盤面の全マス（64マス）を走査
2. 各マスについて `can_place_and_flip` を呼び出し
3. Trueが返された座標をリストに追加
4. リストを返す

### 4.2 8方向の判定

8方向は以下の方向ベクトルで表現します：

```python
directions = [
    (-1, -1), (-1, 0), (-1, 1),  # 左上、上、右上
    (0, -1),           (0, 1),    # 左、右
    (1, -1),  (1, 0),  (1, 1)     # 左下、下、右下
]
```

各方向について、以下の手順で判定します：

1. 隣接マスに相手のコマがあるか確認
2. その方向に進みながら：
   - 相手のコマが続く限り進む
   - 空マスまたは盤面外に到達したらNG
   - 自分のコマに到達したらOK

### 4.3 入出力関数

#### `read_input() -> Tuple[List[List[str]], str]`

標準入力から盤面と手番を読み込みます。

**戻り値**: `(grid, player)` のタプル

**処理**:
```python
def read_input():
    lines = []
    for _ in range(9):
        lines.append(input().strip())

    # 最初の8行が盤面
    grid = [list(line) for line in lines[:8]]

    # 9行目が手番
    player = lines[8]

    return grid, player
```

#### `write_output(grid, legal_moves, player) -> None`

合法手をマークした盤面を標準出力に書き込みます。

**処理**:
```python
def write_output(grid, legal_moves, player):
    # 盤面をコピー
    output_grid = [row[:] for row in grid]

    # 合法手に'0'をマーク
    for row, col in legal_moves:
        output_grid[row][col] = '0'

    # 出力
    for row in output_grid:
        print(''.join(row))
    print(player)
```

## 5. プログラムフロー

### 5.1 メイン処理

```python
def main():
    # 1. 入力読み込み
    grid, player = read_input()

    # 2. 合法手を見つける
    legal_moves = find_legal_moves(grid, player)

    # 3. 結果を出力
    write_output(grid, legal_moves, player)

if __name__ == "__main__":
    main()
```

### 5.2 データの流れ

```
標準入力（9行のテキスト）
    ↓
read_input()
    ↓
grid: List[List[str]], player: str
    ↓
find_legal_moves(grid, player)
    ↓
legal_moves: List[Tuple[int, int]]
    ↓
write_output(grid, legal_moves, player)
    ↓
標準出力（合法手をマークした盤面）
```

## 6. ファイル構成

```
approaches/spec_driven/
├── reversi_core.py         # 合法手判定ロジック
├── reversi.py              # メインプログラム
├── test_reversi.py         # テストコード
├── spec.md                 # 仕様書
├── plan.md                 # 技術計画書（このファイル）
└── README.md               # アプローチ説明
```

### 6.1 reversi_core.py

合法手判定の核となるロジックを含みます：

```python
from typing import List, Tuple

def can_place_and_flip(grid: List[List[str]], row: int, col: int, player: str) -> bool:
    """指定位置が合法手かどうかを判定"""
    pass

def find_legal_moves(grid: List[List[str]], player: str) -> List[Tuple[int, int]]:
    """すべての合法手を見つける"""
    pass
```

### 6.2 reversi.py

入出力と統合処理を含みます：

```python
from typing import List, Tuple
from reversi_core import find_legal_moves

def read_input() -> Tuple[List[List[str]], str]:
    """標準入力から読み込み"""
    pass

def write_output(grid: List[List[str]], legal_moves: List[Tuple[int, int]], player: str) -> None:
    """標準出力に書き込み"""
    pass

def main():
    """メイン処理"""
    grid, player = read_input()
    legal_moves = find_legal_moves(grid, player)
    write_output(grid, legal_moves, player)

if __name__ == "__main__":
    main()
```

### 6.3 test_reversi.py

spec.mdの受入基準に基づくテストコードを含みます：

```python
import pytest
from reversi_core import can_place_and_flip, find_legal_moves

def test_初期配置で黒番の合法手を正しく判定する():
    """AC-001: 初期配置での黒番の合法手判定"""
    pass

def test_初期配置で白番の合法手を正しく判定する():
    """AC-002: 初期配置での白番の合法手判定"""
    pass

def test_合法手がない場合は空リストを返す():
    """AC-003: 合法手がない場合"""
    pass
```

## 7. 実装の詳細

### 7.1 合法手判定アルゴリズム

**can_place_and_flip の実装詳細**:

```python
def can_place_and_flip(grid: List[List[str]], row: int, col: int, player: str) -> bool:
    # 1. 範囲チェック
    if not (0 <= row < 8 and 0 <= col < 8):
        return False

    # 2. 空マスチェック
    if grid[row][col] != '.':
        return False

    # 3. 相手のプレイヤー
    opponent = 'W' if player == 'B' else 'B'

    # 4. 8方向チェック
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    for dr, dc in directions:
        # この方向にひっくり返せるかチェック
        r, c = row + dr, col + dc
        found_opponent = False

        while 0 <= r < 8 and 0 <= c < 8:
            if grid[r][c] == opponent:
                found_opponent = True
                r += dr
                c += dc
            elif grid[r][c] == player and found_opponent:
                return True  # この方向でひっくり返せる
            else:
                break  # 空マスまたは盤面外

    return False  # どの方向でもひっくり返せない
```

### 7.2 エッジケースへの対応

1. **盤面外アクセス**: インデックスの範囲チェック（0 <= index < 8）
2. **合法手がない場合**: 空リストを返す
3. **複数方向にひっくり返せる場合**: 1方向でもOKならTrue

### 7.3 パフォーマンス考慮

- 盤面サイズは8×8固定なので、パフォーマンスは問題にならない
- 全探索（64マス × 8方向）でも十分高速
- 可読性を優先したシンプルな実装

## 8. テスト戦略

### 8.1 受入基準のテスト化

spec.mdの各受入基準（AC-001〜AC-006）をテストケースとして実装します：

| 受入基準 | テスト内容 |
|---------|-----------|
| AC-001 | 初期配置・黒番で4つの合法手を正しく検出 |
| AC-002 | 初期配置・白番で4つの合法手を正しく検出 |
| AC-003 | 合法手がない場合に空リストを返す |
| AC-004 | 複数方向にひっくり返せる場合の判定 |
| AC-005 | 端や角での合法手判定 |
| AC-006 | 入出力の正確性（統合テスト） |

### 8.2 テストデータ

#### 初期配置（黒番）

```python
initial_grid_black = [
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', 'W', 'B', '.', '.', '.'],
    ['.', '.', '.', 'B', 'W', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.']
]

expected_moves_black = [(2, 4), (3, 5), (4, 2), (5, 3)]
```

#### 初期配置（白番）

```python
initial_grid_white = [
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', 'W', 'B', '.', '.', '.'],
    ['.', '.', '.', 'B', 'W', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.']
]

expected_moves_white = [(2, 3), (3, 2), (4, 5), (5, 4)]
```

### 8.3 テスト実行

```bash
# pytestで全テスト実行
pytest test_reversi.py -v

# 特定のテスト実行
pytest test_reversi.py::test_初期配置で黒番の合法手を正しく判定する -v
```

## 9. 実装手順

### フェーズ1: 核となるロジック実装

1. `reversi_core.py` を作成
2. `can_place_and_flip` 関数を実装
3. `find_legal_moves` 関数を実装
4. 単体テストを作成して動作確認

### フェーズ2: 入出力処理実装

1. `reversi.py` を作成
2. `read_input` 関数を実装
3. `write_output` 関数を実装
4. `main` 関数で統合

### フェーズ3: テストと検証

1. `test_reversi.py` を作成
2. spec.mdの受入基準に基づくテストを実装
3. すべてのテストが通ることを確認
4. 手動テスト（問題文の入出力例）

### フェーズ4: ドキュメント作成

1. `README.md` を作成
2. 使い方、テスト方法を記載

## 10. spec.md との対応関係

### 10.1 機能要件との対応

| 機能要件 | 実装 |
|---------|------|
| FR-001: 入力仕様 | `read_input()` 関数 |
| FR-002: 出力仕様 | `write_output()` 関数 |
| FR-003: 合法手の定義 | `can_place_and_flip()` 関数 |
| FR-004: 全方向の判定 | 8方向ループ処理 |

### 10.2 非機能要件との対応

| 非機能要件 | 対応 |
|-----------|------|
| NFR-001: 正確性 | テストによる検証 |
| NFR-002: 使いやすさ | 標準入出力の使用 |
| NFR-003: 拡張性 | 関数の分離、明確なインターフェース |

## 11. まとめ

この技術計画書では、spec.mdで定義された仕様を満たすための実装方針を定義しました：

- **シンプルな設計**: 必要最小限の関数構成
- **明確なデータフロー**: 入力 → 判定 → 出力
- **テスト可能性**: 受入基準をテストコードで検証
- **段階的な実装**: 核となるロジック → 入出力 → 統合

次のフェーズ「Tasks（タスク分解）」では、この計画に基づいて具体的な実装タスクを細分化します。
