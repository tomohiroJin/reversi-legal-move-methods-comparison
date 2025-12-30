"""
Board クラス

リバーシの盤面を表すクラス。
盤面の状態を管理し、セルへのアクセスと基本操作を提供する。
"""

from typing import List


class Board:
    """
    リバーシの盤面を表すクラス

    8x8の盤面を管理し、セルへのアクセスと基本操作を提供する。
    ゲームロジックは含まず、純粋なデータ構造として実装。
    """

    # クラス定数
    EMPTY: str = '.'
    BLACK: str = 'B'
    WHITE: str = 'W'
    SIZE: int = 8

    def __init__(self, grid: List[List[str]]) -> None:
        """
        盤面を初期化する

        Args:
            grid: 8x8の盤面データ（各要素は '.', 'B', 'W' のいずれか）
        """
        # 盤面をディープコピーして保持
        self._grid = [row[:] for row in grid]

    def get_cell(self, row: int, col: int) -> str:
        """
        指定位置のセルの値を取得する

        Args:
            row: 行番号（0-7）
            col: 列番号（0-7）

        Returns:
            セルの値（'.', 'B', 'W' のいずれか）
        """
        return self._grid[row][col]

    def is_valid_position(self, row: int, col: int) -> bool:
        """
        指定位置が盤面内かどうかを判定する

        Args:
            row: 行番号
            col: 列番号

        Returns:
            盤面内なら True、範囲外なら False
        """
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE

    def is_empty(self, row: int, col: int) -> bool:
        """
        指定位置が空マスかどうかを判定する

        Args:
            row: 行番号（0-7）
            col: 列番号（0-7）

        Returns:
            空マスなら True、それ以外なら False
        """
        return self._grid[row][col] == self.EMPTY

    def to_grid(self) -> List[List[str]]:
        """
        内部の盤面データを取得する

        Returns:
            8x8の盤面データ（コピー）
        """
        return [row[:] for row in self._grid]

    @staticmethod
    def get_opponent(player: str) -> str:
        """
        相手プレイヤーを取得する

        Args:
            player: プレイヤー（'B' または 'W'）

        Returns:
            相手プレイヤー（'B' なら 'W'、'W' なら 'B'）
        """
        if player == Board.BLACK:
            return Board.WHITE
        else:
            return Board.BLACK
