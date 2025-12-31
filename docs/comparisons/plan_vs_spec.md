# plan_driven vs spec_driven 比較レポート

## 比較対象
- plan_driven
- spec_driven

## 主要な差分
- 構成: plan_driven は `domain/` と `io/` を分けたレイヤ構成、spec_driven は `reversi_core.py` にロジックを集約
- 仕様整理: plan_driven は `DESIGN.md` を中心に設計を明文化、spec_driven は `spec.md` と `tasks.md` で要件と手順を明確化
- テスト構成: plan_driven は層別に `tests/` を分割、spec_driven は `test_reversi.py` に集約
- テスト件数: plan_driven は 26 件、spec_driven は 14 件
- 進め方: plan_driven はフェーズ分割、spec_driven は BDD/TDD の2重ループ

## 実行結果（README 記載の実行例）
- plan_driven は `...WB...` / `...BW...` の入力
- spec_driven は `...BW...` / `...WB...` の入力
- 入力が異なるため、出力の比較には同一入力が必要

## 備考
- 両方とも `pytest` でテスト実行
- plan_driven は IO とドメインが分離され、spec_driven は仕様ドキュメントとの対応が追いやすい
