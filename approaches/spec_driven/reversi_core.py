# reversi_core.py
# 合法手判定の核となるロジック

from typing import List, Tuple


def can_place_and_flip(grid: List[List[str]], row: int, col: int, player: str) -> bool:
    """
    指定された位置にコマを置くことができ、少なくとも1つ以上の相手のコマを
    ひっくり返せるかを判定する。

    Args:
        grid: 盤面データ（8x8の2次元リスト）
        row: 置く位置の行（0〜7）
        col: 置く位置の列（0〜7）
        player: 現在のプレイヤー（'B' または 'W'）

    Returns:
        bool: 合法手ならTrue、そうでなければFalse
    """
    # 1. 範囲チェック
    if not (0 <= row < 8 and 0 <= col < 8):
        return False

    # 2. 空マスチェック
    if grid[row][col] != '.':
        return False

    # 3. 相手のプレイヤー
    opponent = 'W' if player == 'B' else 'B'

    # 4. 8方向チェック
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # 左上、上、右上
        (0, -1),           (0, 1),    # 左、右
        (1, -1),  (1, 0),  (1, 1)     # 左下、下、右下
    ]

    for dr, dc in directions:
        # この方向にひっくり返せるかチェック
        r, c = row + dr, col + dc
        found_opponent = False

        while 0 <= r < 8 and 0 <= c < 8:
            if grid[r][c] == opponent:
                found_opponent = True
                r += dr
                c += dc
            elif grid[r][c] == player and found_opponent:
                return True  # この方向でひっくり返せる
            else:
                break  # 空マスまたは盤面外

    return False  # どの方向でもひっくり返せない


def find_legal_moves(grid: List[List[str]], player: str) -> List[Tuple[int, int]]:
    """
    指定されたプレイヤーのすべての合法手を見つける。

    Args:
        grid: 盤面データ（8x8の2次元リスト）
        player: 現在のプレイヤー（'B' または 'W'）

    Returns:
        List[Tuple[int, int]]: 合法手の座標リスト
    """
    legal_moves = []

    # 盤面の全マス（64マス）を走査
    for row in range(8):
        for col in range(8):
            # 各マスについて can_place_and_flip を呼び出し
            if can_place_and_flip(grid, row, col, player):
                legal_moves.append((row, col))

    return legal_moves
