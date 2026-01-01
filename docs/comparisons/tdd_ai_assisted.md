# tdd_ai_assisted レビュー

## 概要
- 対象: `approaches/tdd_ai_assisted/`
- 目的: リバーシの合法手判定をTDD+AI支援で実装
- 構成: `Board`（Value Object）と `LegalMoveCalculator` に責務分離、`main.py` で入出力

## 良い点
- 責務分離が明確: `Board` と `LegalMoveCalculator`、I/O が分離されていて追いやすい
- テストが段階的かつ具体的: 1x1〜8x8、縦横斜めなど方向別ケースが揃っている
- 石種を `Enum` 化し、定数化でマジックストリングを減らしている
- 盤面文字列⇔2次元配列の変換が整理されており、主要処理が読みやすい
- README と TODO が揃っていて進め方が見える

## 気になる点・リスク
- `Board` は文字種の検証はあるが、矩形やサイズの検証はしない（`approaches/tdd_ai_assisted/board.py`）。入力生成側で形状保証がある前提なら問題にならないが、外部入力を想定するなら補強余地がある
- `main` の手番入力が `B` 以外なら自動的に `W` 扱いになるため、入力ミスが検出できない（`approaches/tdd_ai_assisted/main.py`）

## テスト・品質
- README 記載では 20 テスト（`test_board.py` 18件、`test_main.py` 2件）
- 不正な手番入力、空入力、行長不一致などのエラーパスは未テスト

## 改善案（優先度順）
- 入力生成側で形状保証がない場合のみ、`Board` で矩形/行長チェックを追加
- `main` で手番のバリデーションを追加し、`B`/`W` 以外は例外にする
- 8x8に限定するならサイズ検証を追加（一般化するならREADMEにサイズ自由である旨を明記）

## 参照
- 実装: `approaches/tdd_ai_assisted/board.py`
- 実装: `approaches/tdd_ai_assisted/legal_move_calculator.py`
- CLI: `approaches/tdd_ai_assisted/main.py`
- テスト: `approaches/tdd_ai_assisted/test_board.py`
- テスト: `approaches/tdd_ai_assisted/test_main.py`
