# plan_driven アプローチ詳細

**特徴**: 事前の詳細な計画とテスト駆動開発（TDD）を組み合わせた実装方法

**4フェーズ・ワークフロー**:
1. **Research（調査）**: 問題の理解と要件の明確化
2. **Plan（計画）**: DESIGN.md と plan.md による詳細な設計と計画の策定
3. **Implement（実装）**: TDD/BDD サイクルに従った段階的な実装
4. **Validate（検証）**: テスト実行、コードレビュー、ドキュメント作成

**主な要素**:
- **事前設計**: DESIGN.md でアーキテクチャと責任分離を明文化
- **計画管理**: plan.md で実装タスクを細分化し、進捗を追跡
- **TDD/BDD**: Red-Green-Refactor サイクルと日本語テスト名による振る舞い駆動開発
- **レイヤードアーキテクチャ**: domain層（ビジネスロジック）と io層（入出力）を分離

**テスト状況**: 全26テストがパス（Board: 6, GameRules: 11, IO層: 6, E2E: 3）

**詳細**: [`approaches/plan_driven/README.md`](../../approaches/plan_driven/README.md)

**Git履歴**: 各コミットが TDD サイクルの完了を表し、実装過程が追跡可能
