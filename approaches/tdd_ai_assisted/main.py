"""
リバーシの合法手を計算するメインモジュール
"""

import sys
from board import Board, Stone
from legal_move_calculator import LegalMoveCalculator


def main():
    """
    標準入力からボードと手番を読み込み、合法手を計算して標準出力に出力する
    """
    # 標準入力から全行を読み込む
    lines = sys.stdin.read().strip().split('\n')

    # 最後の行が手番
    turn_str = lines[-1]

    # それ以外がボード
    board_str = '\n'.join(lines[:-1])

    # 手番を Stone に変換
    turn = Stone.BLACK if turn_str == 'B' else Stone.WHITE

    # Board を作成
    board = Board(board_str)

    # 合法手を計算
    result = LegalMoveCalculator.calculate(board, turn)

    # 標準出力に出力（末尾の改行なし）
    print(result, end='')


if __name__ == '__main__':
    main()
