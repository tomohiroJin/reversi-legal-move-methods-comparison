class Board:
    """リバーシボードクラス"""

    def __init__(self, board: str):
        """ボードを初期化する"""
        Board._validate_board_chars(board)
        self.board = board

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
        validated_chars = {".", "B", "W", "\n"}
        for char in board:
            if char not in validated_chars:
                raise ValueError("ボードには'.', 'B', 'W', '\\n'のみ使用できます。")
