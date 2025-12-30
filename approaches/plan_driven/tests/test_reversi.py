"""
reversi.py のエンドツーエンドテスト

BDD外側のループとしてのテスト。
テスト名は日本語で、プログラム全体が提供すべき振る舞いを表現する。
"""

import sys
import os
import importlib.util
from io import StringIO
from unittest.mock import patch

# reversi モジュールをインポートできるようにパスを追加
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


# reversi.py を手動でインポート
def load_reversi_module():
    """reversi.py を動的にインポートする"""
    reversi_path = os.path.join(parent_dir, 'reversi.py')
    if not os.path.exists(reversi_path):
        return None
    spec = importlib.util.spec_from_file_location("reversi", reversi_path)
    reversi_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reversi_module)
    return reversi_module


def test_初期配置で黒番の合法手を出力する(capsys):
    """
    リバーシの初期配置と黒番を入力として受け取り、
    合法手の位置に '0' をマークした盤面と手番を出力する。
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

    # When: reversi.py のメイン関数を実行
    with patch('sys.stdin', StringIO(入力データ)):
        reversi_module = load_reversi_module()
        if reversi_module is None:
            raise FileNotFoundError("reversi.py が見つかりません")
        reversi_module.main()

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


def test_初期配置で白番の合法手を出力する(capsys):
    """
    リバーシの初期配置と白番を入力として受け取り、
    合法手の位置に '0' をマークした盤面と手番を出力する。
    """
    # Given: 標準入力にリバーシの初期配置と白番が設定されている
    入力データ = """........
........
........
...WB...
...BW...
........
........
........
W"""

    # When: reversi.py のメイン関数を実行
    with patch('sys.stdin', StringIO(入力データ)):
        reversi_module = load_reversi_module()
        if reversi_module is None:
            raise FileNotFoundError("reversi.py が見つかりません")
        reversi_module.main()

    # Then: 合法手位置に '0' がマークされた盤面と手番が出力される
    captured = capsys.readouterr()
    期待する出力 = """........
........
....0...
...WB0..
..0BW...
...0....
........
........
W
"""
    assert captured.out == 期待する出力


def test_合法手がない場合は元の盤面を出力する(capsys):
    """
    合法手が存在しない盤面を入力として受け取り、
    元の盤面をそのまま出力する。
    """
    # Given: 標準入力に合法手がない盤面が設定されている
    入力データ = """BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
W"""

    # When: reversi.py のメイン関数を実行
    with patch('sys.stdin', StringIO(入力データ)):
        reversi_module = load_reversi_module()
        if reversi_module is None:
            raise FileNotFoundError("reversi.py が見つかりません")
        reversi_module.main()

    # Then: 元の盤面と手番が出力される
    captured = capsys.readouterr()
    期待する出力 = """BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
BBBBBBBB
W
"""
    assert captured.out == 期待する出力
