"""
ボードクラスのテストモジュール
"""

# pylint: disable=non-ascii-name,invalid-name

import pytest
from board import Board


class TestBoardCreation:
    """ボード生成のテスト"""

    def test_1x1のボードを設定すると1x1のボードを返却することができる(self):
        """1x1のボードを設定すると1x1のボードを返却することができるテスト"""
        board = Board(".", "B")
        assert str(board) == "."

    def test_1x1のボードにBを最初に配置して返却する(self):
        """1x1のボードにBを最初に配置して返却するテスト"""
        board = Board("B", "B")
        assert str(board) == "B"

    def test_1x1のボードにWを最初に配置して返却する(self):
        """1x1のボードにWを最初に配置して返却するテスト"""
        board = Board("W", "W")
        assert str(board) == "W"

    def test_改行を含むボードを返却する(self):
        """改行を含むボードを返却するテスト"""
        board_str = "....\n.WB.\n.BW.\n...."
        board = Board(board_str, "B")
        assert str(board) == board_str

    def test_8x8のボードにBとWを最初に配置して返却する(self):
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
        board = Board(board_str, "B")
        assert str(board) == board_str


class TestBoardWithPlayer:
    """手番を持つボードのテスト"""

    def test_次の手番にBを設定できて確認することができる(self):
        """次の手番にBを設定できて確認することができるテスト"""
        board = Board(".", "B")
        assert board.player == "B"

    def test_次の手番にWを設定でき確認することができる(self):
        """次の手番にWを設定でき確認することができるテスト"""
        board = Board(".", "W")
        assert board.player == "W"


class TestBoardValidation:
    """ボードバリデーションのテスト"""

    def test_空の場合はエラーが発生する(self):
        """空白の場合はエラーが発生するテスト"""
        with pytest.raises(ValueError, match="ボードには"):
            Board("", "B")

    def test_カンマBW改行以外が設定されている場合はエラーが発生する(self):
        """カンマBW改行以外が設定されている場合はエラーが発生するテスト"""
        with pytest.raises(ValueError, match="ボードには"):
            Board("X", "B")

    def test_次の手番が空の場合エラーが発生する(self):
        """次の手番が空の場合エラーが発生するテスト"""
        with pytest.raises(ValueError, match="手番には"):
            Board(".", "")

    def test_次の手番がBでもWでもない場合エラーが発生する(self):
        """次の手番がBでもWでもない場合エラーが発生するテスト"""
        with pytest.raises(ValueError, match="手番には"):
            Board(".", "X")
