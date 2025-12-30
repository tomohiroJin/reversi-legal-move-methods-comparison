"""
OutputWriter クラスのテスト

振る舞い駆動でテストを記述。
テスト名は日本語で、OutputWriter クラスが提供すべき振る舞いを表現する。
"""

import sys
import os
import importlib.util

# domain と io パッケージをインポートできるようにパスを追加
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from domain.board import Board

# io パッケージは標準ライブラリと名前が競合するため、importlib で手動インポート
io_package_path = os.path.join(parent_dir, 'io')
spec = importlib.util.spec_from_file_location(
    "output_writer",
    os.path.join(io_package_path, "output_writer.py")
)
output_writer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(output_writer_module)
OutputWriter = output_writer_module.OutputWriter


def test_合法手がある場合盤面に0をマークして出力する(capsys):
    """
    合法手のリストが与えられた場合、
    盤面の該当位置に '0' をマークして標準出力に書き込む。
    """
    # Given: リバーシの初期配置と黒番の合法手リスト
    盤面データ = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
    ]
    盤面 = Board(盤面データ)
    合法手リスト = [(2, 3), (3, 2), (4, 5), (5, 4)]
    手番 = 'B'

    # When: OutputWriter で出力する
    ライター = OutputWriter()
    ライター.write_board_with_legal_moves(盤面, 合法手リスト, 手番)

    # Then: 合法手位置に '0' がマークされた盤面と手番が出力される
    captured = capsys.readouterr()
    期待する出力 = """........
........
...0....
..0WB...
...BW0..
....0...
........
........
B
"""
    assert captured.out == 期待する出力


def test_合法手がない場合元の盤面をそのまま出力する(capsys):
    """
    合法手のリストが空の場合、
    元の盤面をそのまま標準出力に書き込む。
    """
    # Given: 盤面と空の合法手リスト
    盤面データ = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
    ]
    盤面 = Board(盤面データ)
    合法手リスト = []
    手番 = 'W'

    # When: OutputWriter で出力する
    ライター = OutputWriter()
    ライター.write_board_with_legal_moves(盤面, 合法手リスト, 手番)

    # Then: 元の盤面と手番が出力される
    captured = capsys.readouterr()
    期待する出力 = """........
........
........
...WB...
...BW...
........
........
........
W
"""
    assert captured.out == 期待する出力


def test_元の盤面は変更されない(capsys):
    """
    OutputWriter は元の盤面を変更せず、
    コピーに '0' をマークして出力する。
    """
    # Given: リバーシの初期配置と合法手リスト
    盤面データ = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
    ]
    盤面 = Board(盤面データ)
    合法手リスト = [(2, 3)]
    手番 = 'B'

    # When: OutputWriter で出力する
    ライター = OutputWriter()
    ライター.write_board_with_legal_moves(盤面, 合法手リスト, 手番)

    # Then: 元の盤面は変更されていない
    assert 盤面.get_cell(2, 3) == '.'
    assert 盤面.get_cell(3, 3) == 'W'
    assert 盤面.get_cell(3, 4) == 'B'
