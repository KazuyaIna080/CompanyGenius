# 🎯 企業名予測システム開発プロジェクトルール v2.0

## 📋 **プロジェクト概要**

### **🎯 プロジェクト名**
`sonet4_integrated_corporate_prediction_system` - 6段階カスケード統合企業名予測システム

### **🏆 プロジェクト目標**
- **精度目標**: 95%予測精度の実現（Phase 14実績: 90.0%）
- **性能目標**: <100ms応答時間（Phase 14実績: 0.3ms）
- **規模目標**: 352万社データベース完全活用（Phase 14達成済み）
- **品質目標**: エラー0%の完璧品質維持（Phase 14達成済み）

### **🧭 現在の状況**
- **完了フェーズ**: Phase 14 Week 2（6段階カスケード統合システム実装完了）
- **現在フェーズ**: `<phase:15_COMMERCIALIZATION>` 商用化・API開発準備
- **次期フェーズ**: Phase 16-20（多言語展開・エコシステム構築）

---

## 🎯 **開発方針（企業名予測システム特化）**

### **本質機能優先戦略**
- **AI/ML統合**: 6段階カスケードシステムの精度・性能最適化
- **大規模データ処理**: 352万社データベースの高速検索・更新
- **API設計**: 商用グレードの予測API・管理API構築
- **UI/UX開発**: 機能確認完了後のChrome拡張・管理画面開発

### **段階的実装方針**
- **本質機能**: アルゴリズム → データベース → API → 統合の順
- **品質保証**: 各段階でエラー0%・文字化け0%の維持
- **性能最適化**: 応答時間・精度・スケーラビリティの同時実現
- **商用化準備**: セキュリティ・認証・監視・ドキュメント完備

---

## 📋 **フェーズ定義（企業名予測システム専用）**

| フェーズ | 内容 | 企業名予測システムでの具体例 | 成果物例 |
|----------|------|---------------------------|----------|
| **01_spec** | 予測要件・精度目標定義 | 「95%精度の実現可能性と手法は？」 | prediction_requirements.md |
| **02_logic** | カスケード統合設計 | 「6段階最適化と新段階追加は？」 | cascade_architecture.drawio |
| **03_api** | 予測API・管理API設計 | 「RESTful API仕様と認証方式は？」 | prediction_api.yaml |
| **04_mock** | Chrome拡張・管理UI設計 | 「ユーザー体験最適化UIは？」 | chrome_extension_mock.sketch |
| **05_impl** | 商用化実装・運用準備 | 「24/7運用とスケーラビリティは？」 | production_deployment/ |

---

## 🏗️ **成果物構成（企業名予測システム専用）**

### **中核システムファイル**
```
enterprise_prediction_system/
├── 01_system_overview.md           # システム全体像・技術仕様
├── 02_cascade_feature_spec.md      # 6段階カスケード機能仕様
├── 03_database_architecture.drawio # 352万社データベース設計
├── 04_prediction_api_design.yaml   # 予測API・管理API仕様
├── 05_ui_chrome_extension.sketch   # Chrome拡張・管理画面設計
│
├── core_systems/                   # 中核システム実装
│   ├── cascade_prediction_engine.py
│   ├── database_search_engine.py
│   ├── integrated_api_server.py
│   └── corporate_master_db/
│
├── performance_logs/               # 性能・品質ログ
│   ├── accuracy_benchmarks.json
│   ├── response_time_logs.csv
│   └── quality_assurance_reports/
│
└── deployment/                     # 商用化・運用準備
    ├── api_documentation/
    ├── security_configuration/
    └── monitoring_dashboards/
```

---

## 🎯 **品質基準（企業名予測システム特化）**

### **🔥 絶対要求事項**
- **精度**: 90%以上維持（目標95%達成）
- **性能**: 100ms以下応答（実績0.3ms維持）
- **品質**: エラー0%・文字化け0%継続
- **可用性**: 99.9%稼働率保証

### **📊 段階別品質ゲート**
```python
# Phase 15品質チェックポイント
def phase15_quality_gate(system_metrics):
    requirements = {
        'accuracy': system_metrics['accuracy'] >= 0.90,
        'response_time': system_metrics['response_time_ms'] <= 100,
        'error_rate': system_metrics['error_rate'] == 0.0,
        'database_integrity': system_metrics['db_errors'] == 0,
        'api_availability': system_metrics['api_uptime'] >= 0.999
    }
    return all(requirements.values())
```

### **🔧 大規模データ処理特化ルール**

#### **S0_352万社データベース品質管理**
- **データ整合性**: 法人番号13桁検証・重複0%維持
- **文字コード統一**: UTF-8完全統一・文字化け0%
- **インデックス最適化**: <100ms検索性能保証
- **バックアップ**: 1日3回自動バックアップ実行

#### **S1_カスケード統合品質管理**
- **段階別検証**: 各カスケードレベルの信頼度検証
- **フォールバック確認**: Level 4-6の正常動作検証
- **統合API**: 単一エンドポイントでの完全機能提供
- **レスポンス品質**: JSON形式・エラーハンドリング完備

---

## 🔄 **Phase 15以降の戦略的ロードマップ**

### **Phase 15: 商用化・API開発 (現在)**
- **95%精度達成**: Level 4-6カスケード本格実装
- **RESTful API**: 商用グレードAPI構築・公開
- **Chrome拡張統合**: ユーザー向け機能完成
- **セキュリティ**: 認証・権限管理・監査ログ

### **Phase 16-17: 市場展開・スケーラビリティ**
- **外部API公開**: 第三者開発者向けAPI提供
- **多言語対応**: 英語・中国語・韓国語企業名対応
- **クラウド展開**: AWS/Azure/GCPでの自動スケーリング
- **SLA保証**: 99.99%可用性・24/7サポート

### **Phase 18-20: エコシステム・業界標準化**
- **プラットフォーム化**: 企業情報統合プラットフォーム
- **業界連携**: 銀行・保険・法務業界との統合
- **AI進化**: GPT統合・自然言語処理強化
- **国際展開**: グローバル企業データベース構築

---

## ⚠️ **プロジェクト固有の注意事項**

### **🚨 絶対禁止事項**
- **精度劣化**: 90%を下回る精度への後退
- **性能劣化**: 100ms超過する応答時間
- **品質劣化**: エラー発生・文字化け発生
- **データ破損**: 352万社データベースの整合性破壊

### **✅ 必須実行事項**
- **段階的検証**: 各Phase完了時の品質ゲート実行
- **性能ベンチマーク**: 毎週の性能測定・記録
- **バックアップ確認**: 毎日のデータベースバックアップ検証
- **セキュリティ監査**: 月次のセキュリティ検査実行

---

## 🔧 **技術スタック（確定版）**

### **中核技術**
- **言語**: Python 3.12 (Windows環境最適化)
- **データベース**: SQLite（352万社・高速インデックス）
- **AI/ML**: LightGBM・カスケード統合システム
- **API**: FastAPI・RESTful・JSON応答

### **開発環境**
- **OS**: Windows 10/11（メイン環境）
- **IDE**: Claude Desktop + MCP拡張機能
- **ハードウェア**: AMD Ryzen 7 5800X + 48GB RAM（実証済み）
- **文字コード**: UTF-8統一・Unicode完全対応

---

## 📝 **進行記録フォーマット（更新版）**

### **Phase完了記録テンプレート**
```markdown
## 《進行記録》<phase:XX_PHASE_NAME> 完了

### 📊 **達成成果**
- **精度**: XX.X% (目標: 95%)
- **性能**: XX.Xms (目標: <100ms)
- **品質**: エラーX件 (目標: 0件)
- **実装**: [完了システム名]

### 🔧 **技術資産**
- **新規ファイル**: [ファイル名リスト]
- **更新DB**: [データベース更新内容]
- **API拡張**: [新規API機能]

### 🎯 **次Phase目標**
- **主目標**: [具体的目標]
- **技術課題**: [解決すべき課題]
- **品質基準**: [達成すべき品質指標]

### 📅 **更新日時**: 2025-XX-XX
```

---

## 🚀 **Claude Desktopでの活用指針**

### **MCP拡張機能活用**
- **filesystem**: 大容量ファイル操作・ログ管理
- **sequential-thinking**: 複雑問題の段階的解決
- **memory**: プロジェクト履歴・設定保存
- **brave_web_search**: 最新技術情報・競合調査

### **開発効率化**
- **50行制限**: ファイル分割での最適実装
- **文字コード注意**: Unicode文字・コメント#の適切処理
- **エラー0%**: Windows環境での完璧動作保証

---

**このプロジェクトルールにより、世界最高水準の企業名予測システムを確実に商用化まで導きます。** 🎯