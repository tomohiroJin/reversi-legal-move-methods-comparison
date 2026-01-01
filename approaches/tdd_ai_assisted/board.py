"""
リバーシのボードを表現するモジュール
"""


class Board:
    """リバーシボードクラス"""

    # ボードで使用可能な文字の定数
    VALID_CHARS = frozenset({".", "B", "W", "\n"})
    # 手番で使用可能な文字の定数
    VALID_PLAYERS = frozenset({"B", "W"})

    def __init__(self, board: str, player: str):
        """ボードを初期化する"""
        Board._validate_board_chars(board)
        Board._validate_player(player)

        self.board = board
        self.player = player

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

    @staticmethod
    def _validate_player(player: str) -> None:
        """
        手番の文字をバリデーションする

        Args:
            player: バリデーション対象の手番文字列

        Raises:
            ValueError: 不正な文字が含まれている場合
        """
        if player not in Board.VALID_PLAYERS:
            raise ValueError("手番には'B'または'W'を指定する必要があります。")
