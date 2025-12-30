"""
リバーシの合法手判定プログラム (vibe_coding アプローチ)

直感的・感覚的にコードを書くアプローチで実装。
まず動くものを作ることを優先し、後からリファクタリングする。
"""

import sys
from typing import List, Tuple


def read_input() -> Tuple[List[List[str]], str]:
    """
    標準入力から盤面と手番を読み込む

    Returns:
        (board, player): 盤面(8x8の2次元リスト)と手番('B' or 'W')
    """
    lines = []
    for line in sys.stdin:
        line = line.rstrip('\n')
        lines.append(line)

    # 最後の行が手番、それ以外が盤面
    player = lines[-1]
    board_lines = lines[:-1]

    # 盤面を2次元リストに変換
    board = []
    for line in board_lines:
        row = list(line)
        board.append(row)

    return board, player


# 8方向のベクトル（上下左右斜め）
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),  # 上方向3つ
    (0, -1),           (0, 1),    # 左右
    (1, -1),  (1, 0),  (1, 1)     # 下方向3つ
]


def can_flip_in_direction(board: List[List[str]], row: int, col: int,
                          dr: int, dc: int, player: str) -> bool:
    """
    特定の方向にコマをひっくり返せるかチェック

    Args:
        board: 盤面
        row: 配置する行
        col: 配置する列
        dr: 行方向の移動量
        dc: 列方向の移動量
        player: 手番('B' or 'W')

    Returns:
        この方向にひっくり返せる場合 True
    """
    # 相手のコマ
    opponent = 'W' if player == 'B' else 'B'

    # この方向に1つ進む
    r, c = row + dr, col + dc

    # 少なくとも1つは相手のコマが必要
    if not (0 <= r < 8 and 0 <= c < 8):
        return False
    if board[r][c] != opponent:
        return False

    # 相手のコマを超えて、自分のコマが見つかるまで進む
    r, c = r + dr, c + dc
    while 0 <= r < 8 and 0 <= c < 8:
        if board[r][c] == '.':
            # 空マスにぶつかった → ひっくり返せない
            return False
        if board[r][c] == player:
            # 自分のコマにぶつかった → ひっくり返せる！
            return True
        # 相手のコマなので、さらに進む
        r, c = r + dr, c + dc

    # 盤面外に出た
    return False


def is_legal_move(board: List[List[str]], row: int, col: int, player: str) -> bool:
    """
    指定位置が合法手かどうかを判定

    Args:
        board: 盤面
        row: 行
        col: 列
        player: 手番

    Returns:
        合法手なら True
    """
    # そのマスが空でなければダメ
    if board[row][col] != '.':
        return False

    # 8方向のうち、少なくとも1方向でひっくり返せればOK
    for dr, dc in DIRECTIONS:
        if can_flip_in_direction(board, row, col, dr, dc, player):
            return True

    return False


def find_legal_moves(board: List[List[str]], player: str) -> List[Tuple[int, int]]:
    """
    全ての合法手を見つける

    Args:
        board: 盤面
        player: 手番

    Returns:
        合法手のリスト [(row, col), ...]
    """
    legal_moves = []

    # 8x8の全マスをチェック
    for row in range(8):
        for col in range(8):
            if is_legal_move(board, row, col, player):
                legal_moves.append((row, col))

    return legal_moves


def print_board_with_legal_moves(board: List[List[str]],
                                   legal_moves: List[Tuple[int, int]],
                                   player: str):
    """
    合法手を0で表示した盤面を出力

    Args:
        board: 盤面
        legal_moves: 合法手のリスト
        player: 手番
    """
    # 出力用の盤面をコピー
    output_board = [row[:] for row in board]

    # 合法手の位置に '0' を配置
    for row, col in legal_moves:
        output_board[row][col] = '0'

    # 出力
    for row in output_board:
        print(''.join(row))
    print(player)


def print_board(board: List[List[str]], player: str):
    """
    盤面を出力する

    Args:
        board: 8x8の盤面
        player: 手番
    """
    for row in board:
        print(''.join(row))
    print(player)


def main():
    """
    メイン処理
    1. 盤面と手番を読み込む
    2. 合法手を見つける
    3. 合法手を0で表示して出力
    """
    board, player = read_input()
    legal_moves = find_legal_moves(board, player)
    print_board_with_legal_moves(board, legal_moves, player)


if __name__ == "__main__":
    main()
