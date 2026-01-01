"""
mainモジュールのテスト
"""

# pylint: disable=non-ascii-name,invalid-name

import io
import sys
from main import main


class TestMain:
    """main関数のテスト"""

    def test_標準入力から8x8ボードと手番を受け取り合法手を標準出力に出力する(self):
        """標準入力から8x8ボードと手番を受け取り合法手を標準出力に出力するテスト"""
        # 入力データ
        input_data = (
            "........\n"
            "........\n"
            "........\n"
            "...BW...\n"
            "...WB...\n"
            "........\n"
            "........\n"
            "........\n"
            "B"
        )

        # 期待される出力
        expected_output = (
            "........\n"
            "........\n"
            "....0...\n"
            "...BW0..\n"
            "..0WB...\n"
            "...0....\n"
            "........\n"
            "........\n"
            "B"
        )

        # 標準入力をモック
        sys.stdin = io.StringIO(input_data)
        # 標準出力をキャプチャ
        sys.stdout = io.StringIO()

        # main関数を実行
        main()

        # 出力を取得
        output = sys.stdout.getvalue()

        # 標準入出力を復元
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

        # 検証
        assert output == expected_output

    def test_標準入力から3x1ボードと手番を受け取り合法手を標準出力に出力する(self):
        """標準入力から3x1ボードと手番を受け取り合法手を標準出力に出力するテスト"""
        # 入力データ
        input_data = "BW.\nB"

        # 期待される出力
        expected_output = "BW0\nB"

        # 標準入力をモック
        sys.stdin = io.StringIO(input_data)
        # 標準出力をキャプチャ
        sys.stdout = io.StringIO()

        # main関数を実行
        main()

        # 出力を取得
        output = sys.stdout.getvalue()

        # 標準入出力を復元
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

        # 検証
        assert output == expected_output
