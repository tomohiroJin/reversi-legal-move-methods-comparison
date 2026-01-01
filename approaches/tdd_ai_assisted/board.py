"""
リバーシのボードを表現するモジュール
"""

from enum import Enum


class Stone(Enum):
    """リバーシの石の列挙型"""

    BLACK = "B"
    WHITE = "W"


class Board:
    """リバーシボードクラス"""

    # ボードで使用可能な文字の定数
    VALID_CHARS = frozenset({".", Stone.BLACK.value, Stone.WHITE.value, "\n"})

    def __init__(self, board: str, turn: Stone):
        """ボードを初期化する"""
        Board._validate_board_chars(board)

        self.board = board
        self.turn = turn

    def with_legal_moves(self) -> str:
        """合法手を含むボード表示を返す"""
        return f"{self.board}\n{self.turn.value}"

    def __str__(self):
        return self.board

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
