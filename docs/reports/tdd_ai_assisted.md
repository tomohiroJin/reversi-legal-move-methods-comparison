# tdd_ai_assisted レポート

## 対象
- アプローチ: tdd_ai_assisted
- 課題: `problem/problem_statement.md`

## ディレクトリ内容
- `board.py`
- `legal_move_calculator.py`
- `main.py`
- `test_board.py`
- `test_main.py`
- `README.md`
- `TODO.md`
- `requirements.txt`

## 作り方（README/TODO から要約）
- ケント・ベック流の Red-Green-Refactor を軸に段階的に拡張
- 1x1 -> 3x1/1x3 -> 斜め -> 8方向 -> 8x8 という順でスコープを広げる
- Board と LegalMoveCalculator を分離し、Value Object で不変性を確保
- TODO にタスクの完了履歴が残り、進行が追跡可能

## Git 履歴から見える進め方
- README にはテスト数と実装順序が明記されているが、Git 履歴の詳細は未確認
- TODO のチェックリストで TDD の進行が追いやすい

## 実装内容の分析
- `Board` は盤面文字列を保持し、文字種の検証と変換（文字列<->2次元配列）を担当
- `Stone` を Enum 化し、手番の表現を安全にしている
- `LegalMoveCalculator` は 8 方向ベクトルで合法手を探索し、`_check_direction` で方向判定を集約
- `main` は標準入力を読み込み、最後の行を手番として扱い結果を出力
- 合法手は盤面内で `0` にマークし、手番を最終行に出力

## 実行結果（README 記載の手順）

### 実行コマンド
```bash
python main.py <<'INPUT'
........
........
........
...BW...
...WB...
........
........
........
B
INPUT
```

### 出力
```
........
........
....0...
...BW0..
..0WB...
...0....
........
........
B
```

### テスト
```bash
python -m pytest -q
```

```
20 passed
```
