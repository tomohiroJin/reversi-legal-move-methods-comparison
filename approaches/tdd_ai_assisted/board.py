"""
リバーシのボードを表現するモジュール
"""

from enum import Enum


class Stone(Enum):
    """リバーシの石の列挙型"""

    BLACK = "B"
    WHITE = "W"


class Board:
    """ボードの盤面状態を表す Value Object"""

    # 空きマスを表す定数
    EMPTY = "."

    # ボードで使用可能な文字の定数
    VALID_CHARS = frozenset({EMPTY, Stone.BLACK.value, Stone.WHITE.value, "\n"})

    def __init__(self, board: str):
        """ボードを初期化する"""
        Board._validate_board_chars(board)
        self._board = board

    @property
    def board(self) -> str:
        """ボード文字列を取得する（読み取り専用）"""
        return self._board

    def __str__(self):
        return self._board

    @staticmethod
    def string_to_array(board_str: str) -> list[list[str]]:
        """
        ボード文字列を2次元配列に変換する

        Args:
            board_str: ボード文字列

        Returns:
            2次元配列（list[list[str]]）
        """
        lines = board_str.split("\n")
        return [list(line) for line in lines]

    @staticmethod
    def array_to_string(board: list[list[str]]) -> str:
        """
        2次元配列をボード文字列に変換する

        Args:
            board: 2次元配列

        Returns:
            ボード文字列
        """
        return "\n".join("".join(row) for row in board)

    @staticmethod
    def _validate_board_chars(board: str) -> None:
        """
        ボードの文字をバリデーションする

        Args:
            board: バリデーション対象のボード文字列

        Raises:
            ValueError: 不正な文字が含まれている場合
        """
        if not board:
            raise ValueError("ボードには少なくとも1文字必要です。")
        for char in board:
            if char not in Board.VALID_CHARS:
                valid_chars_str = ", ".join(repr(c) for c in sorted(Board.VALID_CHARS))
                raise ValueError(f"ボードには{valid_chars_str}のみ使用できます。")
