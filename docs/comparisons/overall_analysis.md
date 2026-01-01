# 全アプローチ比較レポート

## 対象
- plan_driven
- spec_driven
- tdd_ai_assisted
- vibe_coding

## 比較軸
- 構成（モジュール分割・責務分離）
- 入出力設計と前提
- 合法手判定アルゴリズム
- テスト戦略/件数
- ドキュメント/進め方
- リスク/制約

## 比較サマリ（マトリクス）
| 観点 | plan_driven | spec_driven | tdd_ai_assisted | vibe_coding |
|---|---|---|---|---|
| 構成 | domain/io 分離 + entry | core/entry の2分割 | Board + Calculator + main | 単一スクリプト |
| 盤面表現 | 8x8 2次元配列 | 8x8 2次元配列 | 文字列（改行含む） | 8x8 2次元配列 |
| 入力前提 | 8行+手番固定 | 9行固定 | 最終行が手番 | 最終行が手番 |
| アルゴリズム | 8方向チェック（GameRules） | 8方向チェック（関数） | 8方向チェック（方向ベクトル） | 8方向チェック（方向ベクトル） |
| テスト件数 | 26 | 14 | 20 | 9 |
| テスト粒度 | 層別 + E2E | 統合+ユニット混在 | Board/計算/CLI | 単体中心 |
| ドキュメント | DESIGN/plan/README | spec/plan/tasks/README | README/TODO | README |
| 進め方 | 4フェーズ + TDD/BDD | 2重ループ | TDD + AI協働 | 実装先行 |

## 主要な比較ポイント

### 1. 構成と責務分離
- **plan_driven**: `domain/` と `io/` を分離し、`reversi.py` は統合のみ。責務分離が最も明確で拡張しやすい。
- **spec_driven**: `reversi_core.py` にロジックを集約し、`reversi.py` で入出力。シンプルだが拡張時は分離が必要。
- **tdd_ai_assisted**: `Board` と `LegalMoveCalculator` に分割し、`main.py` がI/O。クラス分割は明確。
- **vibe_coding**: 単一スクリプトで完結。理解は容易だが拡張や差分管理には不利。

### 2. 入力設計と前提
- **plan_driven/spec_driven**: 8x8固定で読み込む設計。入力サイズや文字種の検証は実装上は限定的。
- **tdd_ai_assisted**: `Board` が文字種（`.`, `B`, `W`, 改行）を検証するが、矩形性やサイズは保証しない。`main` は `B` 以外を `W` とみなす挙動。
- **vibe_coding**: EOF まで読み込み、最後の行を手番として扱う。サイズや文字種の検証はない。

### 3. 合法手判定アルゴリズム
- 全アプローチ共通で 8 方向ベクトルを用いた標準的な挟み込み判定。
- **plan_driven**: `GameRules.can_flip_in_direction` を中心に段階的にTDD。
- **tdd_ai_assisted**: `_check_direction` で方向判定を集約し、`_is_legal_move` から呼び出す構造。

### 4. テスト戦略と網羅性
- **plan_driven**: 26件。Board/Rules/IO/E2E の層別テストがあり最も網羅的。
- **spec_driven**: 14件。受入基準（AC）を意識した統合+ユニットの一体設計。
- **tdd_ai_assisted**: 20件。1x1から8方向まで段階的に広げるテスト構成。
- **vibe_coding**: 9件。最小限の確認に留まり、境界系や入力エラー系は薄い。

### 5. ドキュメントと進め方
- **plan_driven**: DESIGN と plan を起点に、フェーズごとの進行が明確。履歴追跡性が高い。
- **spec_driven**: spec/plan/tasks の三点セットで仕様から実装まで一貫。
- **tdd_ai_assisted**: README と TODO に TDD の進行が残る。AI協働の過程が読み取りやすい。
- **vibe_coding**: README のみ。実装優先でドキュメントは最小限。

## 評価（強みと弱み）

### plan_driven
- 強み: 拡張性・保守性が最も高い。責務分離とテストの層が揃っている。
- 弱み: 構成が重く、学習コストと実装コストは高め。

### spec_driven
- 強み: 仕様とテストの対応が追いやすい。構成がシンプルで理解が早い。
- 弱み: モジュール分割が浅く、拡張時に再設計が必要。

### tdd_ai_assisted
- 強み: TDDの段階的な拡張が明確。Board/Calculator分離でロジックが追いやすい。
- 弱み: 入力バリデーションの前提が薄く、CLIの手番解釈が単純。

### vibe_coding
- 強み: 実装速度と読みやすさ（単一ファイル）が高い。
- 弱み: テストと設計が薄く、変更耐性は低い。

## 総合所見
- **品質重視/拡張前提なら plan_driven** が最も堅牢。
- **仕様と実装の対応を素早く作るなら spec_driven** が効率的。
- **TDD学習や段階的拡張の教材なら tdd_ai_assisted** が適切。
- **最短で動作確認したい場合は vibe_coding** が向くが、長期運用には不向き。

