# spec_driven vs vibe_coding 比較レポート

## 比較対象
- spec_driven
- vibe_coding

## 主要な差分
- 構成: spec_driven は `reversi_core.py` を分離、vibe_coding は単一スクリプト構成
- ドキュメント: spec_driven は `spec.md` / `plan.md` / `tasks.md`、vibe_coding は `README.md` に集約
- テスト: どちらも `test_reversi.py` 単体だが、spec_driven は受入基準の統合テストが明示的
- テスト件数: spec_driven は 14 件、vibe_coding は 9 件
- 進め方: spec_driven は仕様とタスクから開始、vibe_coding は実装中心で後からテスト追加

## 実行結果（README 記載の実行例）
- 入力例は同一（`...BW...` / `...WB...`）
- 出力は同一

## 備考
- 両方とも `pytest` でテスト実行
- spec_driven は仕様ドキュメントと実装対応が明確、vibe_coding は実装速度重視
