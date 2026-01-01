"""
ボードクラスのテストモジュール
"""

# pylint: disable=non-ascii-name,invalid-name

import pytest
from board import Board


def test_1x1のボードを設定すると1x1のボードを返却することができる():
    """1x1のボードを設定すると1x1のボードを返却することができるテスト"""
    board = Board(".")
    assert str(board) == "."


def test_1x1のボードにBを最初に配置して返却する():
    """1x1のボードにBを最初に配置して返却するテスト"""
    board = Board("B")
    assert str(board) == "B"


def test_1x1のボードにWを最初に配置して返却する():
    """1x1のボードにWを最初に配置して返却するテスト"""
    board = Board("W")
    assert str(board) == "W"


def test_改行を含むボードを返却する():
    """改行を含むボードを返却するテスト"""
    board_str = "....\n.WB.\n.BW.\n...."
    board = Board(board_str)
    assert str(board) == board_str


def test_カンマBW改行以外が設定されている場合はエラーが発生する():
    """カンマBW改行以外が設定されている場合はエラーが発生するテスト"""
    with pytest.raises(ValueError, match="ボードには"):
        Board("X")


def test_8x8のボードにBとWを最初に配置して返却する():
    """8x8のボードにBとWを最初に配置して返却するテスト"""
    board_str = (
        "........\n"
        "........\n"
        "........\n"
        "...BW...\n"
        "...WB...\n"
        "........\n"
        "........\n"
        "........"
    )
    board = Board(board_str)
    assert str(board) == board_str
