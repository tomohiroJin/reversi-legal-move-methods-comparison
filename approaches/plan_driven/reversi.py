"""
リバーシ合法手判定プログラム

標準入力から盤面と手番を読み込み、
合法手の位置に '0' をマークした盤面を標準出力に書き込む。
"""

import sys
import os
import importlib.util


def main() -> None:
    """
    メイン処理

    1. 標準入力から盤面と手番を読み込む
    2. 合法手を計算する
    3. 合法手をマークして標準出力に書き込む
    """
    # domain モジュールをインポート
    from domain.board import Board
    from domain.game_rules import GameRules

    # io パッケージは標準ライブラリと競合するため、importlib で手動インポート
    current_dir = os.path.dirname(os.path.abspath(__file__))
    io_package_path = os.path.join(current_dir, 'io')

    # InputReader をインポート
    input_reader_spec = importlib.util.spec_from_file_location(
        "input_reader",
        os.path.join(io_package_path, "input_reader.py")
    )
    input_reader_module = importlib.util.module_from_spec(input_reader_spec)
    input_reader_spec.loader.exec_module(input_reader_module)
    InputReader = input_reader_module.InputReader

    # OutputWriter をインポート
    output_writer_spec = importlib.util.spec_from_file_location(
        "output_writer",
        os.path.join(io_package_path, "output_writer.py")
    )
    output_writer_module = importlib.util.module_from_spec(output_writer_spec)
    output_writer_spec.loader.exec_module(output_writer_module)
    OutputWriter = output_writer_module.OutputWriter

    # 1. 標準入力から盤面と手番を読み込む
    リーダー = InputReader()
    盤面, 手番 = リーダー.read_from_stdin()

    # 2. 合法手を計算する
    ルール = GameRules(盤面)
    合法手リスト = ルール.find_all_legal_moves(手番)

    # 3. 合法手をマークして標準出力に書き込む
    ライター = OutputWriter()
    ライター.write_board_with_legal_moves(盤面, 合法手リスト, 手番)


if __name__ == "__main__":
    main()
