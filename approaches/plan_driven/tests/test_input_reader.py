"""
InputReader クラスのテスト

振る舞い駆動でテストを記述。
テスト名は日本語で、InputReader クラスが提供すべき振る舞いを表現する。
"""

import sys
import os
import io as _stdlib_io
import importlib.util
from unittest.mock import patch

# domain と io パッケージをインポートできるようにパスを追加
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from domain.board import Board

# io パッケージは標準ライブラリと名前が競合するため、importlib で手動インポート
io_package_path = os.path.join(parent_dir, 'io')
spec = importlib.util.spec_from_file_location(
    "input_reader",
    os.path.join(io_package_path, "input_reader.py")
)
input_reader_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(input_reader_module)
InputReader = input_reader_module.InputReader

# StringIO は標準ライブラリから取得
StringIO = _stdlib_io.StringIO


def test_標準入力から盤面と手番を正しく読み込める():
    """
    標準入力から8行の盤面データと1行の手番を読み込み、
    Board オブジェクトと手番文字列を返す。
    """
    # Given: 標準入力にリバーシの初期配置と黒番が設定されている
    入力データ = """........
........
........
...WB...
...BW...
........
........
........
B"""

    # When: 標準入力から読み込む
    with patch('sys.stdin', StringIO(入力データ)):
        リーダー = InputReader()
        盤面, 手番 = リーダー.read_from_stdin()

    # Then: Board オブジェクトが正しく構築される
    assert 盤面.get_cell(3, 3) == 'W'
    assert 盤面.get_cell(3, 4) == 'B'
    assert 盤面.get_cell(4, 3) == 'B'
    assert 盤面.get_cell(4, 4) == 'W'
    assert 盤面.get_cell(0, 0) == '.'

    # Then: 手番が正しく読み込まれる
    assert 手番 == 'B'


def test_白番の盤面を正しく読み込める():
    """
    標準入力から白番の盤面を読み込める。
    """
    # Given: 標準入力に白番が設定されている
    入力データ = """........
........
........
...WB...
...BW...
........
........
........
W"""

    # When: 標準入力から読み込む
    with patch('sys.stdin', StringIO(入力データ)):
        リーダー = InputReader()
        盤面, 手番 = リーダー.read_from_stdin()

    # Then: 手番が正しく読み込まれる
    assert 手番 == 'W'


def test_任意の盤面配置を正しく読み込める():
    """
    初期配置以外の任意の盤面配置も正しく読み込める。
    """
    # Given: 標準入力にカスタム盤面が設定されている
    入力データ = """BBBBBBBB
WWWWWWWW
........
...WB...
...BW...
........
BBBBBBBB
WWWWWWWW
B"""

    # When: 標準入力から読み込む
    with patch('sys.stdin', StringIO(入力データ)):
        リーダー = InputReader()
        盤面, 手番 = リーダー.read_from_stdin()

    # Then: カスタム盤面が正しく読み込まれる
    assert 盤面.get_cell(0, 0) == 'B'
    assert 盤面.get_cell(0, 7) == 'B'
    assert 盤面.get_cell(1, 0) == 'W'
    assert 盤面.get_cell(1, 7) == 'W'
    assert 盤面.get_cell(2, 0) == '.'
    assert 盤面.get_cell(6, 0) == 'B'
    assert 盤面.get_cell(7, 0) == 'W'
