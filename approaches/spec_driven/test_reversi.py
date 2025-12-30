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
...WB...
...BW...
........
........
........
B"""

    # 期待される出力
    expected_output = """........
........
....0...
...WB0..
..0BW...
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
