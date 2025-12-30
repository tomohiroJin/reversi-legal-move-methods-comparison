# vibe_coding

リバーシの合法手判定プログラムを **vibe_coding アプローチ** で実装しました。

## 目次

- [アプローチ概要](#アプローチ概要)
- [セットアップ](#セットアップ)
- [実行方法](#実行方法)
- [テスト実行](#テスト実行)
- [入出力フォーマット](#入出力フォーマット)
- [実装の特徴](#実装の特徴)
- [実装の過程](#実装の過程)
- [ファイル構成](#ファイル構成)

---

## アプローチ概要

### vibe_coding とは

**vibe_coding** は「直感的・感覚的にコードを書く」開発アプローチです。
厳密な仕様書や詳細な計画を先に立てることなく、コードを書きながら理解を深め、必要に応じてリファクタリングしていきます。

### 特徴

- **コードファースト**: 計画書より先にコードを書く
- **最小限の構造**: 必要になるまで複雑な構造は作らない
- **直感的な実装**: 読みやすさと分かりやすさを重視
- **反復的改善**: 動くものを作ってから改善する

### 他のアプローチとの違い

| アプローチ | 特徴 |
|-----------|------|
| **spec_driven** | 仕様を先に定義 → vibe_coding は仕様より先にコード |
| **tdd_ai_assisted** | テストファースト → vibe_coding は実装ファースト |
| **plan_driven** | 詳細計画を立てる → vibe_coding は計画より実装 |
| **vibe_coding** | 直感的にコードを書く、後からテストとリファクタリング |

### このアプローチが向いている場面

- 問題が比較的明確で、試行錯誤しながら進めたい場合
- プロトタイプを素早く作りたい場合
- 要件が変わりやすく、柔軟性が必要な場合

---

## セットアップ

### 前提条件

- Python 3.11.2 以上

### インストール手順

```bash
cd approaches/vibe_coding
pip install -r requirements.txt
```

---

## 実行方法

### 標準入力から実行

```bash
python reversi.py
```

実行後、以下の形式で盤面と手番を入力してください：

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

### ファイルから実行

```bash
python reversi.py < input.txt
```

### 実行例

```bash
$ cat <<'EOF' | python reversi.py
........
........
........
...BW...
...WB...
........
........
........
B
EOF

# 出力:
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

---

## テスト実行

### 全テスト実行

```bash
pytest test_reversi.py -v
```

### 特定のテストのみ実行

```bash
pytest test_reversi.py::test_initial_position -v
```

### テスト結果

```
============================= test session starts ==============================
test_reversi.py::test_initial_position PASSED                            [ 11%]
test_reversi.py::test_white_initial_position PASSED                      [ 22%]
test_reversi.py::test_no_legal_moves PASSED                              [ 33%]
test_reversi.py::test_corner_position PASSED                             [ 44%]
test_reversi.py::test_multiple_directions PASSED                         [ 55%]
test_reversi.py::test_edge_positions PASSED                              [ 66%]
test_reversi.py::test_can_flip_in_direction_basic PASSED                 [ 77%]
test_reversi.py::test_is_legal_move_occupied PASSED                      [ 88%]
test_reversi.py::test_all_eight_directions PASSED                        [100%]

============================== 9 passed in 0.02s ===============================
```

---

## 入出力フォーマット

### 入力形式

- 8行の盤面（各行8文字）
  - `.`: 空マス
  - `B`: 黒のコマ
  - `W`: 白のコマ
- 最後の行に手番（`B` または `W`）

### 出力形式

- 8行の盤面（各行8文字）
  - 合法手の位置に `0` を表示
  - それ以外は入力と同じ
- 最後の行に手番

### 例

**入力:**
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

**出力:**
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

この例では、黒（`B`）の合法手が4つあります：
- `(2, 4)`: 下方向に白をひっくり返せる
- `(3, 5)`: 左方向に白をひっくり返せる
- `(4, 2)`: 右方向に白をひっくり返せる
- `(5, 3)`: 上方向に白をひっくり返せる

---

## 実装の特徴

### コード構造

**単一ファイル構成**: reversi.py に全ての実装を集約

主要な関数:
1. `read_input()`: 標準入力から盤面と手番を読み込む
2. `can_flip_in_direction()`: 特定の方向にコマをひっくり返せるかチェック
3. `is_legal_move()`: 指定位置が合法手かどうかを判定
4. `find_legal_moves()`: 全ての合法手を見つける
5. `print_board_with_legal_moves()`: 合法手を0で表示して出力

### 8方向チェックのアルゴリズム

リバーシでは、コマを配置した時に8方向（上下左右斜め）にひっくり返せるかをチェックする必要があります。

```python
# 8方向のベクトル（上下左右斜め）
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),  # 上方向3つ
    (0, -1),           (0, 1),    # 左右
    (1, -1),  (1, 0),  (1, 1)     # 下方向3つ
]
```

各方向について、以下の条件を満たす場合に「ひっくり返せる」と判定：
1. 隣接するマスに相手のコマがある
2. その方向に進んで、相手のコマが1つ以上連続している
3. 相手のコマの向こう側に自分のコマがある

### vibe_coding らしいポイント

- **直感的な関数名**: `can_flip_in_direction`, `is_legal_move` など、何をするか一目で分かる
- **日本語コメント**: 思考の流れをコメントに残す
- **最小限の抽象化**: クラスを使わず、関数ベースで実装
- **後からテスト**: TDDではなく、実装後にテストを書いて検証

---

## 実装の過程

vibe_coding アプローチでの実装の流れを記録します。

### Phase 1: 骨組み作成

**最初のステップ**: 入力を読んで出力するだけのプログラムを作成

```python
def read_input():
    # 標準入力から盤面と手番を読み込む
    pass

def print_board(board, player):
    # 盤面を出力する
    pass

def main():
    board, player = read_input()
    print_board(board, player)
```

この時点で動作確認。入力がそのまま出力されることを確認。

### Phase 2: コア機能実装

**8方向チェックの実装**: 最初は1方向だけ実装して動作確認してから、8方向に拡張

```python
def can_flip_in_direction(board, row, col, dr, dc, player):
    # 1. 相手のコマを定義
    # 2. 隣接マスが相手のコマかチェック
    # 3. その方向に進んで自分のコマが見つかるまで探索
    pass
```

**合法手判定**: 8方向のうち1つでもひっくり返せればOK

```python
def is_legal_move(board, row, col, player):
    if board[row][col] != '.':
        return False
    for dr, dc in DIRECTIONS:
        if can_flip_in_direction(board, row, col, dr, dc, player):
            return True
    return False
```

**全マスをチェック**: シンプルに8x8をループ

```python
def find_legal_moves(board, player):
    legal_moves = []
    for row in range(8):
        for col in range(8):
            if is_legal_move(board, row, col, player):
                legal_moves.append((row, col))
    return legal_moves
```

### Phase 3: テストとバグ修正

**テスト作成**: 問題文の例を最優先でテスト化

最初のテスト失敗:
- `test_no_legal_moves`: テストケースの設計ミス。盤面を修正。
- `test_multiple_directions`: (2,2) を空マスにし忘れ。修正。

**全テストがパス**: 9つのテストケース全てがパス

### Phase 4: リファクタリング

今回は特にリファクタリングの必要がなかった。
- コードは十分読みやすい
- 関数分割も適切
- パフォーマンスも問題なし（8x8の盤面なので）

### 学んだこと

1. **コードを書きながら理解が深まる**: 最初は「8方向チェック」が曖昧だったが、実装しながら明確になった
2. **テストで設計ミスを発見**: テストを書くことで、自分の理解不足が明らかになった
3. **最小限の構造で十分**: クラスを使わなくても、関数だけで十分に実装できた
4. **日本語コメントの価値**: 思考を日本語で残すことで、後から見返しやすい

---

## ファイル構成

```
approaches/vibe_coding/
├── README.md              # このファイル
├── requirements.txt       # pytest のみ
├── reversi.py            # メイン実装（約180行）
└── test_reversi.py       # テストコード（約220行、9テストケース）
```

### reversi.py の構成

| 関数名 | 行数 | 説明 |
|-------|-----|------|
| `read_input()` | 15行 | 標準入力から盤面と手番を読み込む |
| `can_flip_in_direction()` | 30行 | 特定の方向にひっくり返せるかチェック |
| `is_legal_move()` | 15行 | 指定位置が合法手かどうか判定 |
| `find_legal_moves()` | 15行 | 全ての合法手を見つける |
| `print_board_with_legal_moves()` | 20行 | 合法手を0で表示して出力 |
| `print_board()` | 10行 | 盤面を出力 |
| `main()` | 10行 | メイン処理 |

### test_reversi.py のテストケース

1. `test_initial_position`: 問題文の初期配置
2. `test_white_initial_position`: 白番の初期配置
3. `test_no_legal_moves`: 合法手がない場合
4. `test_corner_position`: 角への配置
5. `test_multiple_directions`: 複数方向に同時にひっくり返せる
6. `test_edge_positions`: 盤面の端
7. `test_can_flip_in_direction_basic`: can_flip_in_direction の基本テスト
8. `test_is_legal_move_occupied`: 既にコマがあるマス
9. `test_all_eight_directions`: 8方向全てのチェック

---

## まとめ

vibe_coding アプローチでリバーシの合法手判定プログラムを実装しました。

### 良かった点

- **素早いプロトタイピング**: 骨組みから完成まで約4時間で実装完了
- **シンプルな構造**: 単一ファイル、関数ベースで十分に実装できた
- **高い可読性**: 日本語コメントと分かりやすい関数名で、誰でも理解しやすい

### 改善の余地

- **テストファースト**: TDDで書いていれば、テストケースの設計ミスを早期に発見できた
- **エラーハンドリング**: 不正な入力に対するエラー処理は未実装
- **パフォーマンス**: 最適化は行っていないが、8x8の盤面では問題なし

### 他のアプローチとの比較ポイント

今後、他のアプローチ（spec_driven, tdd_ai_assisted, plan_driven）と比較すると、以下の観点で違いが見えてくるはずです：

- **開発速度**: vibe_coding は最も早く動くプロトタイプができる可能性
- **コードの構造**: より自由な構造 vs より厳格な構造
- **バグの発見タイミング**: 実装後 vs 実装中（TDD）
- **リファクタリングの必要性**: 後から改善 vs 最初から良い設計

vibe_coding は、問題が明確で素早くプロトタイプを作りたい場合に最適なアプローチでした。
