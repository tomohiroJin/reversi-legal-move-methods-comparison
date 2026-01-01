"""
リバーシの合法手を計算するモジュール
"""

from board import Board, Stone


class LegalMoveCalculator:
    """合法手を計算するクラス"""

    # 合法手を表す定数
    LEGAL_MOVE_MARK = "0"

    @staticmethod
    def calculate(board: Board, turn: Stone) -> str:
        """
        合法手を計算する

        Args:
            board: ボードの盤面状態
            turn: 現在の手番

        Returns:
            合法手をマークしたボード表示と手番
        """
        board_array = Board.string_to_array(board.board)
        LegalMoveCalculator._mark_legal_moves(board_array, turn)
        legal_moves_board = Board.array_to_string(board_array)
        return f"{legal_moves_board}\n{turn.value}"

    @staticmethod
    def _mark_legal_moves(board: list[list[str]], turn: Stone) -> None:
        """
        2次元配列に合法手をマークする

        Args:
            board: ボードの2次元配列（直接変更される）
            turn: 現在の手番
        """
        height = len(board)
        width = len(board[0]) if height > 0 else 0

        my_stone = turn.value
        opponent_stone = LegalMoveCalculator._get_opponent_stone(turn)

        # 全ての空きマスをチェック
        for y in range(height):
            for x in range(width):
                # 空きマス以外はスキップ
                if board[y][x] != Board.EMPTY:
                    continue

                if LegalMoveCalculator._is_legal_move(board, x, y, my_stone, opponent_stone):
                    board[y][x] = LegalMoveCalculator.LEGAL_MOVE_MARK

    @staticmethod
    def _is_legal_move(
        board: list[list[str]], x: int, y: int, my_stone: str, opponent_stone: str
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
        # チェックする方向のリスト（8方向）
        directions = [
            (-1, 0),   # 左
            (1, 0),    # 右
            (0, -1),   # 上
            (0, 1),    # 下
            (-1, -1),  # 左上
            (1, -1),   # 右上
            (-1, 1),   # 左下
            (1, 1),    # 右下
        ]

        for dx, dy in directions:
            if LegalMoveCalculator._check_direction(board, x, y, dx, dy, my_stone, opponent_stone):
                return True

        return False

    @staticmethod
    def _check_direction(
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
