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

    # 空きマスを表す定数
    EMPTY = "."
    # 合法手を表す定数
    LEGAL_MOVE_MARK = "0"

    # ボードで使用可能な文字の定数
    VALID_CHARS = frozenset({EMPTY, Stone.BLACK.value, Stone.WHITE.value, "\n"})

    def __init__(self, board: str, turn: Stone):
        """ボードを初期化する"""
        Board._validate_board_chars(board)

        self.board = board
        self.turn = turn

    def with_legal_moves(self) -> str:
        """合法手を含むボード表示を返す"""
        board = Board._string_to_board_array(self.board)
        self._mark_legal_moves(board)
        legal_moves_board = Board._board_array_to_string(board)
        return f"{legal_moves_board}\n{self.turn.value}"

    def _mark_legal_moves(self, board: list[list[str]]) -> None:
        """
        2次元配列に合法手をマークする

        Args:
            board: ボードの2次元配列（直接変更される）
        """
        height = len(board)
        width = len(board[0]) if height > 0 else 0

        my_stone = self.turn.value
        opponent_stone = Board._get_opponent_stone(self.turn)

        # 全ての空きマスをチェック
        for y in range(height):
            for x in range(width):
                # 空きマス以外はスキップ
                if board[y][x] != Board.EMPTY:
                    continue

                if self._is_legal_move(board, x, y, my_stone, opponent_stone):
                    board[y][x] = Board.LEGAL_MOVE_MARK

    def _is_legal_move(
        self, board: list[list[str]], x: int, y: int, my_stone: str, opponent_stone: str
    ) -> bool:
        """
        特定位置が合法手かどうかを判定

        Args:
            board: ボードの2次元配列
            x: X座標
            y: Y座標
            my_stone: 自分の石
            opponent_stone: 相手の石

        Returns:
            合法手の場合True
        """
        # 左方向 (-1, 0)
        if self._check_direction(board, x, y, -1, 0, my_stone, opponent_stone):
            return True

        # 上方向 (0, -1)
        if self._check_direction(board, x, y, 0, -1, my_stone, opponent_stone):
            return True

        return False

    def _check_direction(
        self,
        board: list[list[str]],
        x: int,
        y: int,
        dx: int,
        dy: int,
        my_stone: str,
        opponent_stone: str,
    ) -> bool:
        """
        特定方向に合法手かチェック

        Args:
            board: ボードの2次元配列
            x: X座標
            y: Y座標
            dx: X方向の増分 (-1=左, 0=変化なし, 1=右)
            dy: Y方向の増分 (-1=上, 0=変化なし, 1=下)
            my_stone: 自分の石
            opponent_stone: 相手の石

        Returns:
            その方向に合法手がある場合True
        """
        height = len(board)
        width = len(board[0]) if height > 0 else 0

        # 隣接マスが相手の石かチェック
        next_x = x + dx
        next_y = y + dy

        if next_x < 0 or next_x >= width or next_y < 0 or next_y >= height:
            return False

        if board[next_y][next_x] != opponent_stone:
            return False

        # その先に自分の石があるかチェック
        step = 2
        while True:
            check_x = x + dx * step
            check_y = y + dy * step

            if check_x < 0 or check_x >= width or check_y < 0 or check_y >= height:
                return False

            if board[check_y][check_x] == my_stone:
                return True
            elif board[check_y][check_x] != opponent_stone:
                return False

            step += 1

    def __str__(self):
        return self.board

    @staticmethod
    def _get_opponent_stone(turn: Stone) -> str:
        """
        相手の石を取得する

        Args:
            turn: 現在の手番

        Returns:
            相手の石の文字列
        """
        return Stone.WHITE.value if turn == Stone.BLACK else Stone.BLACK.value

    @staticmethod
    def _string_to_board_array(board_str: str) -> list[list[str]]:
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
    def _board_array_to_string(board: list[list[str]]) -> str:
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
