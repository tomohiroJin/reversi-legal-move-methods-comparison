# plan_driven vs vibe_coding 比較レポート

## 比較対象
- plan_driven
- vibe_coding

## 主要な差分
- 構成: plan_driven は `domain/` と `io/` を分けたレイヤ構成、vibe_coding は単一スクリプト構成
- ドキュメント: plan_driven は `DESIGN.md` / `plan.md` を中心、vibe_coding は `README.md` に集約
- テスト: plan_driven は層別テスト、vibe_coding は `test_reversi.py` 単体
- テスト件数: plan_driven は 26 件、vibe_coding は 9 件
- 進め方: plan_driven はフェーズ分割、vibe_coding は実装を先に進めて後からテストを追加

## 実行結果（README 記載の実行例）
- plan_driven は `...WB...` / `...BW...` の入力
- vibe_coding は `...BW...` / `...WB...` の入力
- 入力が異なるため、出力の比較には同一入力が必要

## 備考
- 両方とも `pytest` でテスト実行
- plan_driven は責務分離が明確、vibe_coding は理解しやすい単一ファイル構成
