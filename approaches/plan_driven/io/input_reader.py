"""
InputReader クラス

標準入力からリバーシの盤面と手番を読み込む。
"""

import sys
from typing import Tuple
from domain.board import Board


class InputReader:
    """
    標準入力から盤面と手番を読み込むクラス

    8行の盤面データと1行の手番を標準入力から読み込み、
    Board オブジェクトと手番を返す。
    """

    def read_from_stdin(self) -> Tuple[Board, str]:
        """
        標準入力から盤面と手番を読み込む

        標準入力から以下のフォーマットで読み込む:
        - 8行: 盤面データ（各行8文字、'.', 'B', 'W' のいずれか）
        - 1行: 手番（'B' または 'W'）

        Returns:
            (Board, str): 盤面オブジェクトと手番のタプル
        """
        # 8行の盤面データを読み込む
        盤面データ = []
        for _ in range(Board.SIZE):
            行 = sys.stdin.readline().strip()
            盤面データ.append(list(行))

        # 1行の手番を読み込む
        手番 = sys.stdin.readline().strip()

        # Board オブジェクトを構築
        盤面 = Board(盤面データ)

        return 盤面, 手番
