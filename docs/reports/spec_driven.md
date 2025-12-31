# spec_driven レポート

## 対象
- アプローチ: spec_driven
- 課題: `problem/problem_statement.md`

## ディレクトリ内容
- `reversi.py` / `reversi_core.py`
- `spec.md` / `plan.md` / `tasks.md` / `README.md`
- `test_reversi.py`

## 作り方（README から要約）
- `spec.md` に受入基準（AC-001〜）を Given-When-Then で整理
- `plan.md` でデータ構造と関数設計、手順を明文化
- `tasks.md` で実装をタスク分解し、BDD/TDD の 2 重ループで進める
- 実装とテストを段階的に拡張し、最後に README を整備

## Git 履歴から見える進め方
- 仕様/計画/タスクを先に積み、テスト -> 実装 -> リファクタの順で進行
- 代表的な流れ:
  - `6d82dd2` spec.md 作成
  - `dd09f4c` / `11b04be` plan.md の策定/再整理
  - `0327d73` / `4de4614` tasks の作成と2重ループ化
  - `9381287` 以降で Red/Green/Refactor を段階的に実施
  - `c5dc7cf` で全テストと手動確認
  - `278cdd7` README 追加、`eb16a66` で仕上げ

## 実装内容の分析
- ロジックは `reversi_core.py` に集中し、入出力は `reversi.py` に分離
- コアは `can_place_and_flip` と `find_legal_moves` の2関数が中心
- 受入基準に紐づく統合テストが `test_reversi.py` に集約
- 構成がシンプルで、仕様と実装の対応が追いやすい

## 実行結果（README 記載の手順）

### 実行コマンド
```bash
python reversi.py <<'EOF'
........
........
........
...BW...
...WB...
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
python -m pytest test_reversi.py -q
```

```
14 passed in 0.04s
```
