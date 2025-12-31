# reversi.py
# メインプログラム（入出力と統合）

from typing import List, Tuple
from reversi_core import find_legal_moves


def read_input() -> Tuple[List[List[str]], str]:
    """
    標準入力から盤面と手番を読み込む。

    Returns:
        Tuple[List[List[str]], str]: (盤面データ, 手番)
    """
    lines = []
    for _ in range(9):
        lines.append(input().strip())

    # 最初の8行が盤面
    grid = [list(line) for line in lines[:8]]

    # 9行目が手番
    player = lines[8]

    return grid, player


def write_output(grid: List[List[str]], legal_moves: List[Tuple[int, int]], player: str) -> None:
    """
    合法手をマークした盤面を標準出力に書き込む。

    Args:
        grid: 盤面データ
        legal_moves: 合法手の座標リスト
        player: 手番
    """
    # 盤面をコピー
    output_grid = [row[:] for row in grid]

    # 合法手に'0'をマーク
    for row, col in legal_moves:
        output_grid[row][col] = '0'

    # 出力
    for row in output_grid:
        print(''.join(row))
    print(player)


def main():
    """
    メイン処理：標準入力から盤面を読み込み、合法手を見つけて出力する。
    """
    # 1. 入力読み込み
    grid, player = read_input()

    # 2. 合法手を見つける
    legal_moves = find_legal_moves(grid, player)

    # 3. 結果を出力
    write_output(grid, legal_moves, player)


if __name__ == "__main__":
    main()
