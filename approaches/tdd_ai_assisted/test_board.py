"""
ボードクラスのテストモジュール
"""

# pylint: disable=non-ascii-name,invalid-name

import pytest
from board import Board, Stone


class TestBoardCreation:
    """ボード生成のテスト"""

    def test_1x1のボードを設定すると1x1のボードを返却することができる(self):
        """1x1のボードを設定すると1x1のボードを返却することができるテスト"""
        board = Board(".", Stone.BLACK)
        assert str(board) == "."

    def test_1x1のボードにBを最初に配置して返却する(self):
        """1x1のボードにBを最初に配置して返却するテスト"""
        board = Board("B", Stone.BLACK)
        assert str(board) == "B"

    def test_1x1のボードにWを最初に配置して返却する(self):
        """1x1のボードにWを最初に配置して返却するテスト"""
        board = Board("W", Stone.WHITE)
        assert str(board) == "W"

    def test_改行を含むボードを返却する(self):
        """改行を含むボードを返却するテスト"""
        board_str = "....\n.WB.\n.BW.\n...."
        board = Board(board_str, Stone.BLACK)
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
        board = Board(board_str, Stone.BLACK)
        assert str(board) == board_str

    def test_次の手番にBを設定できて確認することができる(self):
        """次の手番にBを設定できて確認することができるテスト"""
        board = Board(".", Stone.BLACK)
        assert board.turn == Stone.BLACK

    def test_次の手番にWを設定でき確認することができる(self):
        """次の手番にWを設定でき確認することができるテスト"""
        board = Board(".", Stone.WHITE)
        assert board.turn == Stone.WHITE


class TestBoardLegalMoves:
    """合法手を含むボード表示のテスト"""

    def test_合法な手が存在しない場合はボードがそのまま出力され最後に手番の石が表示される(
        self,
    ):
        """合法な手が存在しない場合はボードがそのまま出力され最後に手番の石が表示されるテスト"""
        board_str = (
            "BBBBBBBB\n"
            "BBBBBBBB\n"
            "BBBBBBBB\n"
            "BBBBBBBB\n"
            "BBBBBBBB\n"
            "BBBBBBBB\n"
            "BBBBBBBB\n"
            "BBBBBBBB"
        )
        board = Board(board_str, Stone.WHITE)
        assert board.with_legal_moves() == board_str + "\nW"

    def test_3x1でBWが左から並んでB手番の場合にBW0が出力される(self):
        """3x1でBWが左から並んでB手番の場合にBW0が出力されるテスト"""
        board_str = "BW."
        board = Board(board_str, Stone.BLACK)
        assert board.with_legal_moves() == "BW0\nB"

    def test_3x1でWBが左から並んでW手番の場合にWB0が出力される(self):
        """3x1でWBが左から並んでW手番の場合にWB0が出力されるテスト"""
        board_str = "WB."
        board = Board(board_str, Stone.WHITE)
        assert board.with_legal_moves() == "WB0\nW"

    def test_4x1でBWWが左から並んでB手番の場合にBWW0が出力される(self):
        """4x1でBWWが左から並んでB手番の場合にBWW0が出力されるテスト"""
        board_str = "BWW."
        board = Board(board_str, Stone.BLACK)
        assert board.with_legal_moves() == "BWW0\nB"

    def test_1x3でBWが上から並んでB手番の場合にBW0が出力される(self):
        """1x3でBWが上から並んでB手番の場合にBW0が出力されるテスト"""
        board_str = "B\nW\n."
        board = Board(board_str, Stone.BLACK)
        assert board.with_legal_moves() == "B\nW\n0\nB"

    def test_1x3でWBが上から並んでW手番の場合にWB0が出力される(self):
        """1x3でWBが上から並んでW手番の場合にWB0が出力されるテスト"""
        board_str = "W\nB\n."
        board = Board(board_str, Stone.WHITE)
        assert board.with_legal_moves() == "W\nB\n0\nW"

    def test_1x4でBWWが上から並んでB手番の場合にBWW0が出力される(self):
        """1x4でBWWが上から並んでB手番の場合にBWW0が出力されるテスト"""
        board_str = "B\nW\nW\n."
        board = Board(board_str, Stone.BLACK)
        assert board.with_legal_moves() == "B\nW\nW\n0\nB"

    def test_3x3で左上からBWが並んでB手番の場合にBW0が出力される(self):
        """3x3で左上からBWが並んでB手番の場合にBW0が出力されるテスト"""
        board_str = "B..\n.W.\n..."
        board = Board(board_str, Stone.BLACK)
        assert board.with_legal_moves() == "B..\n.W.\n..0\nB"


class TestBoardValidation:
    """ボードバリデーションのテスト"""

    def test_空の場合はエラーが発生する(self):
        """空白の場合はエラーが発生するテスト"""
        with pytest.raises(ValueError, match="ボードには"):
            Board("", Stone.BLACK)

    def test_カンマBW改行以外が設定されている場合はエラーが発生する(self):
        """カンマBW改行以外が設定されている場合はエラーが発生するテスト"""
        with pytest.raises(ValueError, match="ボードには"):
            Board("X", Stone.BLACK)
