"""
OutputWriter クラス

リバーシの盤面と合法手を標準出力に書き込む。
"""

import sys
from typing import List, Tuple
from domain.board import Board


class OutputWriter:
    """
    盤面と合法手を標準出力に書き込むクラス

    盤面をコピーし、合法手の位置に '0' をマークして出力する。
    元の盤面は変更しない。
    """

    def write_board_with_legal_moves(
        self,
        board: Board,
        legal_moves: List[Tuple[int, int]],
        player: str
    ) -> None:
        """
        盤面と合法手を標準出力に書き込む

        盤面をコピーし、合法手の位置に '0' をマークして出力する。
        最後に手番を出力する。

        Args:
            board: 盤面
            legal_moves: 合法手のリスト [(row, col), ...]
            player: 手番（'B' または 'W'）
        """
        # 盤面をコピー
        盤面データ = board.to_grid()

        # 合法手の位置に '0' をマーク
        for row, col in legal_moves:
            盤面データ[row][col] = '0'

        # 盤面を出力
        for 行 in 盤面データ:
            sys.stdout.write(''.join(行) + '\n')

        # 手番を出力
        sys.stdout.write(player + '\n')
