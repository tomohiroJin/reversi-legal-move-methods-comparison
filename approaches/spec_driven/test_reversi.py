# test_reversi.py
# リバーシ合法手判定プログラムのテストコード

import pytest
from io import StringIO
import sys


# === 外側のループ1: AC-001（初期配置・黒番の合法手判定）===

def test_初期配置で黒番の合法手を正しく表示する():
    """
    Given: 盤面が初期配置である
    And: 手番が黒（B）である
    When: プログラムを実行する
    Then: 4箇所の合法手が '0' でマークされる
    """
    # 入力データ（初期配置・黒番）
    input_data = """........
........
........
...BW...
...WB...
........
........
........
B"""

    # 期待される出力
    expected_output = """........
........
....0...
...BW0..
..0WB...
...0....
........
........
B
"""

    # 標準入力を置き換え
    sys.stdin = StringIO(input_data)

    # 標準出力をキャプチャ
    captured_output = StringIO()
    sys.stdout = captured_output

    # プログラムを実行
    from reversi import main
    main()

    # 出力を取得
    actual_output = captured_output.getvalue()

    # 標準入出力を元に戻す
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__

    # 検証
    assert actual_output == expected_output, f"Expected:\n{expected_output}\nActual:\n{actual_output}"


# === 外側のループ2: AC-002（初期配置・白番の合法手判定）===

def test_初期配置で白番の合法手を正しく表示する():
    """
    Given: 盤面が初期配置である
    And: 手番が白（W）である
    When: プログラムを実行する
    Then: 4箇所の合法手が '0' でマークされる
    """
    # 入力データ（初期配置・白番）
    input_data = """........
........
........
...BW...
...WB...
........
........
........
W"""

    # 期待される出力
    expected_output = """........
........
...0....
..0BW...
...WB0..
....0...
........
........
W
"""

    # 標準入力を置き換え
    sys.stdin = StringIO(input_data)

    # 標準出力をキャプチャ
    captured_output = StringIO()
    sys.stdout = captured_output

    # プログラムを実行
    from reversi import main
    main()

    # 出力を取得
    actual_output = captured_output.getvalue()

    # 標準入出力を元に戻す
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__

    # 検証
    assert actual_output == expected_output, f"Expected:\n{expected_output}\nActual:\n{actual_output}"


# === 外側のループ3: AC-003（合法手がない場合）===

def test_合法手がない場合は0をマークしない():
    """
    Given: 盤面上にどこに置いても相手のコマがひっくり返らない状態
    When: プログラムを実行する
    Then: 出力された盤面に '0' のマークがない
    """
    # 入力データ（すべて黒で埋まっている盤面・白番）
    input_data = """BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
W"""

    # 期待される出力（'0' がない）
    expected_output = """BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
W
"""

    # 標準入力を置き換え
    sys.stdin = StringIO(input_data)

    # 標準出力をキャプチャ
    captured_output = StringIO()
    sys.stdout = captured_output

    # プログラムを実行
    from reversi import main
    main()

    # 出力を取得
    actual_output = captured_output.getvalue()

    # 標準入出力を元に戻す
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__

    # 検証（'0' がないことを確認）
    assert '0' not in actual_output
    assert actual_output == expected_output, f"Expected:\n{expected_output}\nActual:\n{actual_output}"


# === 外側のループ4: AC-004, AC-005（エッジケース）===

def test_複数方向にひっくり返せる場合も正しく判定する():
    """AC-004: 1つの手で複数方向にひっくり返せる場合"""
    from reversi_core import can_place_and_flip

    # 角に置く場合、複数方向にひっくり返せる盤面
    # (0, 0) に黒を置くと、右、下、右下の3方向にひっくり返せる
    grid = [
        ['.', 'W', 'B', '.', '.', '.', '.', '.'],  # 右方向: . W B（OK）
        ['W', 'W', 'B', '.', '.', '.', '.', '.'],  # 右下方向: . W B（OK）
        ['B', '.', '.', '.', '.', '.', '.', '.'],  # 下方向: . W B（OK）
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]

    # (0, 0) に黒を置くと、右、下、右下の3方向にひっくり返せる
    assert can_place_and_flip(grid, 0, 0, 'B') == True


def test_端や角での合法手判定がエラーなく動作する():
    """AC-005: 盤面の端や角でも正しく判定"""
    from reversi_core import can_place_and_flip

    # 初期配置の盤面
    grid = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]

    # 角や端でエラーなく判定できる
    assert can_place_and_flip(grid, 0, 0, 'B') == False  # 左上角
    assert can_place_and_flip(grid, 0, 7, 'B') == False  # 右上角
    assert can_place_and_flip(grid, 7, 0, 'B') == False  # 左下角
    assert can_place_and_flip(grid, 7, 7, 'B') == False  # 右下角
    assert can_place_and_flip(grid, 0, 3, 'B') == False  # 上端
    assert can_place_and_flip(grid, 7, 3, 'B') == False  # 下端
    assert can_place_and_flip(grid, 3, 0, 'B') == False  # 左端
    assert can_place_and_flip(grid, 3, 7, 'B') == False  # 右端


# === 内側のループ1-A: can_place_and_flip 関数（TDD）===

def test_空マスで相手のコマを挟める場合は合法手と判定する():
    """隣接マスに相手のコマがあり、その先に自分のコマがある場合"""
    from reversi_core import can_place_and_flip

    # 初期配置の盤面
    grid = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]

    # 黒番で (2, 4) は合法手（下方向にWを挟める）
    assert can_place_and_flip(grid, 2, 4, 'B') == True


def test_既にコマがある位置は合法手ではないと判定する():
    """空マスでない場合は False"""
    from reversi_core import can_place_and_flip

    grid = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]

    # (3, 3) には既に 'B' がある
    assert can_place_and_flip(grid, 3, 3, 'B') == False


def test_どの方向にも相手のコマを挟めない場合は合法手ではないと判定する():
    """8方向すべてチェックしても挟めない場合は False"""
    from reversi_core import can_place_and_flip

    grid = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]

    # (0, 0) は孤立しているので挟めない
    assert can_place_and_flip(grid, 0, 0, 'B') == False


def test_盤面外の位置は合法手ではないと判定する():
    """範囲外の座標は False"""
    from reversi_core import can_place_and_flip

    grid = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]

    # 盤面外（row < 0, row >= 8, col < 0, col >= 8）
    assert can_place_and_flip(grid, -1, 0, 'B') == False
    assert can_place_and_flip(grid, 8, 0, 'B') == False
    assert can_place_and_flip(grid, 0, -1, 'B') == False
    assert can_place_and_flip(grid, 0, 8, 'B') == False


# === 内側のループ1-B: find_legal_moves 関数（TDD）===

def test_初期配置で黒番は4つの合法手を持つ():
    """初期配置・黒番の場合、(2,4), (3,5), (4,2), (5,3) が合法手"""
    from reversi_core import find_legal_moves

    # 初期配置の盤面
    grid = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]

    legal_moves = find_legal_moves(grid, 'B')
    expected = [(2, 4), (3, 5), (4, 2), (5, 3)]

    # セットとして比較（順序は問わない）
    assert set(legal_moves) == set(expected)
    assert len(legal_moves) == 4


def test_初期配置で白番は4つの合法手を持つ():
    """初期配置・白番の場合、(2,3), (3,2), (4,5), (5,4) が合法手"""
    from reversi_core import find_legal_moves

    # 初期配置の盤面
    grid = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]

    legal_moves = find_legal_moves(grid, 'W')
    expected = [(2, 3), (3, 2), (4, 5), (5, 4)]

    # セットとして比較（順序は問わない）
    assert set(legal_moves) == set(expected)
    assert len(legal_moves) == 4


def test_合法手がない場合は空リストを返す():
    """どこにも置けない盤面の場合、[] を返す"""
    from reversi_core import find_legal_moves

    # すべて黒で埋まっている盤面（白は置けない）
    grid = [
        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
        ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B']
    ]

    legal_moves = find_legal_moves(grid, 'W')
    assert legal_moves == []


# === 内側のループ1-C: 入出力処理（TDD）===

def test_標準入力から盤面と手番を読み込める():
    """9行の入力を盤面データと手番に変換"""
    from reversi import read_input

    # 標準入力をシミュレート
    input_data = """........
........
........
...BW...
...WB...
........
........
........
B"""

    sys.stdin = StringIO(input_data)

    grid, player = read_input()

    # 標準入力を元に戻す
    sys.stdin = sys.__stdin__

    # 盤面データの検証
    assert len(grid) == 8
    assert len(grid[0]) == 8
    assert grid[3][3] == 'B'
    assert grid[3][4] == 'W'
    assert grid[4][3] == 'W'
    assert grid[4][4] == 'B'

    # 手番の検証
    assert player == 'B'


def test_合法手をマークした盤面を出力できる():
    """合法手に'0'をマークして出力"""
    from reversi import write_output

    # 初期配置の盤面
    grid = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]

    legal_moves = [(2, 4), (3, 5), (4, 2), (5, 3)]
    player = 'B'

    # 標準出力をキャプチャ
    captured_output = StringIO()
    sys.stdout = captured_output

    write_output(grid, legal_moves, player)

    # 標準出力を元に戻す
    sys.stdout = sys.__stdout__

    # 出力内容を検証
    output = captured_output.getvalue()
    expected = """........
........
....0...
...BW0..
..0WB...
...0....
........
........
B
"""

    assert output == expected
