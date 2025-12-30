# test_reversi.py
# リバーシ合法手判定プログラムのテストコード

import pytest
from io import StringIO
import sys


# === 外側のループ1: AC-001（初期配置・黒番の合法手判定）===

def test_初期配置で黒番の合法手を正しく表示する():
    """
    Given: 盤面が初期配置である
    And: 手番が黒（B）である
    When: プログラムを実行する
    Then: 4箇所の合法手が '0' でマークされる
    """
    # 入力データ（初期配置・黒番）
    input_data = """........
........
........
...WB...
...BW...
........
........
........
B"""

    # 期待される出力
    expected_output = """........
........
....0...
...WB0..
..0BW...
...0....
........
........
B
"""

    # 標準入力を置き換え
    sys.stdin = StringIO(input_data)

    # 標準出力をキャプチャ
    captured_output = StringIO()
    sys.stdout = captured_output

    # プログラムを実行
    from reversi import main
    main()

    # 出力を取得
    actual_output = captured_output.getvalue()

    # 標準入出力を元に戻す
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__

    # 検証
    assert actual_output == expected_output, f"Expected:\n{expected_output}\nActual:\n{actual_output}"
