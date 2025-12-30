"""
GameRules クラス

リバーシのゲームルールを実装するクラス。
合法手の判定と全合法手の列挙を行う。
"""

from typing import List, Tuple
from domain.board import Board


class GameRules:
    """
    リバーシのゲームルールを実装するクラス

    盤面を受け取り、合法手の判定と列挙を行う。
    盤面の状態は変更せず、純粋な判定のみを行う。
    """

    # 8方向のベクトル（上下左右斜め）
    DIRECTIONS: List[Tuple[int, int]] = [
        (-1, -1), (-1, 0), (-1, 1),  # 上方向3つ
        (0, -1),           (0, 1),    # 左右
        (1, -1),  (1, 0),  (1, 1)     # 下方向3つ
    ]

    def __init__(self, board: Board) -> None:
        """
        GameRules を初期化する

        Args:
            board: 判定対象の盤面
        """
        self._board = board

    def can_flip_in_direction(
        self,
        row: int,
        col: int,
        dr: int,
        dc: int,
        player: str
    ) -> bool:
        """
        特定の方向にコマをひっくり返せるかを判定する

        指定位置から指定方向に進み、以下の条件を満たすか確認:
        1. 隣接マスに相手のコマがある
        2. その方向に相手のコマが1つ以上連続
        3. 相手のコマの向こう側に自分のコマがある

        Args:
            row: 配置する行（0-7）
            col: 配置する列（0-7）
            dr: 行方向の移動量（-1, 0, 1）
            dc: 列方向の移動量（-1, 0, 1）
            player: 手番（'B' または 'W'）

        Returns:
            この方向にひっくり返せる場合 True、それ以外 False
        """
        # 相手のコマ
        opponent = Board.get_opponent(player)

        # この方向に1つ進む
        r, c = row + dr, col + dc

        # 少なくとも1つは相手のコマが必要
        if not self._board.is_valid_position(r, c):
            return False
        if self._board.get_cell(r, c) != opponent:
            return False

        # 相手のコマを超えて、自分のコマが見つかるまで進む
        r, c = r + dr, c + dc
        while self._board.is_valid_position(r, c):
            cell = self._board.get_cell(r, c)
            if cell == Board.EMPTY:
                # 空マスにぶつかった → ひっくり返せない
                return False
            if cell == player:
                # 自分のコマにぶつかった → ひっくり返せる！
                return True
            # 相手のコマなので、さらに進む
            r, c = r + dr, c + dc

        # 盤面外に出た
        return False

    def is_legal_move(self, row: int, col: int, player: str) -> bool:
        """
        指定位置が合法手かどうかを判定する

        合法手の条件:
        1. そのマスが空である
        2. 8方向のうち少なくとも1方向でコマをひっくり返せる

        Args:
            row: 行（0-7）
            col: 列（0-7）
            player: 手番（'B' または 'W'）

        Returns:
            合法手なら True、それ以外 False
        """
        # そのマスが空でなければダメ
        if not self._board.is_empty(row, col):
            return False

        # 8方向のうち、少なくとも1方向でひっくり返せればOK
        for dr, dc in self.DIRECTIONS:
            if self.can_flip_in_direction(row, col, dr, dc, player):
                return True

        return False
