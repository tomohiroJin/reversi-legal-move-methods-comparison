# plan_driven レポート

## 対象
- アプローチ: plan_driven
- 課題: `problem/problem_statement.md`

## ディレクトリ内容
- `reversi.py`（エントリポイント）
- `requirements.txt`（pytest のみ）
- `domain/`（盤面/ルール）
- `io/`（入出力）
- `tests/`（ユニット/結合/E2E）
- `DESIGN.md` / `plan.md` / `README.md`

## 作り方（README から要約）
- フェーズ0で構成と設計を準備し、`DESIGN.md` と `plan.md` を先に作成
- フェーズ1〜3で TDD を適用（Board -> GameRules -> IO）
- フェーズ4で E2E を追加し、統合レイヤで完成度を担保
- フェーズ5で README とルート README を整備

## Git 履歴から見える進め方
- 初期化後、Board -> GameRules -> IO -> reversi.py の順で積み上げ
- 各フェーズごとにコミットが分割され、TDD サイクル単位で履歴が残る
- 代表的な流れ:
  - `b0b5faf` 初期セットアップ
  - `c3d8654` Board を TDD で実装
  - `4c8bf46` / `fc2f439` / `a8b57a5` GameRules の段階実装
  - `6971c0f` / `ad136e5` IO レイヤ実装
  - `5a9863b` エントリポイント実装
  - `e528afa` / `fcd5c9d` 進捗と完了の記録

## 実装内容の分析
- 役割分離: `domain` にロジック、`io` に入出力、`reversi.py` は統合のみ
- 盤面は `Board` クラスで保持し、定数（EMPTY/BLACK/WHITE/SIZE）で意味を明確化
- ルールは `GameRules` に閉じ込め、方向チェックや合法手判定をメソッド化
- IO は `InputReader` / `OutputWriter` に分離され、テスト対象を限定可能
- テストは層ごとに分割され、網羅性が高い

## 実行結果（README 記載の手順）

### 実行コマンド
```bash
python reversi.py <<'EOF'
........
........
........
...WB...
...BW...
........
........
........
B
EOF
```

### 出力
```
........
........
...0....
..0WB...
...BW0..
....0...
........
........
B
```

### テスト
```bash
python -m pytest tests/ -q
```

```
26 passed in 0.07s
```
