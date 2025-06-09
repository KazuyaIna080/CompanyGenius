# 🔧 Project Config Templates v1.0
## プロジェクトタイプ別設定テンプレート集

---

## 📋 **Template 1: AI/ML予測システム（企業名予測システム版）**

```markdown
## PROJECT_CONFIG_BLOCK_START

### 🎯 プロジェクト基本情報
- **PROJECT_NAME**: integrated_corporate_prediction_system
- **PROJECT_TYPE**: AI/ML Prediction System
- **CURRENT_PHASE**: <phase:15_COMMERCIALIZATION>
- **TARGET_GOALS**: 95%予測精度・<100ms応答・352万社データベース活用

### 🔧 技術スタック
- **LANGUAGE**: Python 3.12
- **DATABASE**: SQLite（352万レコード・高速インデックス）
- **ML_FRAMEWORK**: LightGBM・6段階カスケード統合
- **API_FRAMEWORK**: FastAPI・RESTful・JSON応答
- **TOOLS**: pandas・numpy・scikit-learn

### 📊 品質基準
- **PERFORMANCE_TARGET**: <100ms応答（実績0.3ms）
- **ACCURACY_TARGET**: 95%予測精度（実績90.0%）
- **QUALITY_REQUIREMENTS**: エラー0%・文字化け0%・可用性99.9%
- **SPECIAL_RULES**: 大規模データ品質管理・カスケード統合制御

### 🔄 フェーズ定義（AI/ML特化）
| フェーズ | AI/MLでの内容 | 具体例 |
|----------|--------------|--------|
| 01_DISCOVERY | 予測要件・精度目標定義 | 「95%精度の実現可能性は？」 |
| 02_ANALYSIS | データ分析・特徴量設計 | 「最適な特徴量組合せは？」 |
| 03_ARCHITECTURE | ML統合・カスケード設計 | 「6段階統合の最適構造は？」 |
| 04_INTERFACE | 予測API・管理API設計 | 「RESTful予測APIの仕様は？」 |
| 05_IMPLEMENTATION | ML統合・商用化実装 | 「本番グレード品質は？」 |
| 06_VALIDATION | 精度検証・性能測定 | 「目標精度・性能達成は？」 |
| 07_EXTENSION | 多言語・多地域展開 | 「グローバル対応は？」 |

### 📁 成果物構成（AI/ML特化）
```
ai_ml_prediction_system/
├── 01_prediction_requirements.md      # 予測要件・精度目標
├── 02_data_analysis_feature_spec.md   # データ分析・特徴量仕様
├── 03_ml_cascade_architecture.drawio  # ML統合・カスケード設計
├── 04_prediction_api_design.yaml      # 予測API・管理API仕様
├── 05_ml_implementation/              # ML実装・統合コード
│   ├── cascade_prediction_engine.py
│   ├── database_search_engine.py
│   ├── integrated_api_server.py
│   └── data_processing/
├── quality_ml_assurance/              # ML品質保証
│   ├── accuracy_benchmarks.json
│   ├── performance_metrics.csv
│   ├── model_validation_reports/
│   └── data_quality_logs/
└── deployment_ml/                     # ML本番展開
    ├── model_serving/
    ├── monitoring_dashboards/
    └── scaling_configuration/
```

## PROJECT_CONFIG_BLOCK_END
```

---

## 📋 **Template 2: Webアプリケーション**

```markdown
## PROJECT_CONFIG_BLOCK_START

### 🎯 プロジェクト基本情報
- **PROJECT_NAME**: modern_web_application
- **PROJECT_TYPE**: Full-Stack Web Application
- **CURRENT_PHASE**: <phase:03_ARCHITECTURE>
- **TARGET_GOALS**: 高UX・レスポンシブ・SEO最適化

### 🔧 技術スタック
- **LANGUAGE**: TypeScript・Python
- **DATABASE**: PostgreSQL・Redis（キャッシュ）
- **FRONTEND**: React・Next.js・Tailwind CSS
- **BACKEND**: FastAPI・SQLAlchemy
- **TOOLS**: Vite・ESLint・Prettier・Jest

### 📊 品質基準
- **PERFORMANCE_TARGET**: <2s初期読み込み・<500msページ遷移
- **ACCESSIBILITY_TARGET**: WCAG 2.1 AA準拠
- **QUALITY_REQUIREMENTS**: テストカバレッジ85%・SEOスコア90+
- **SPECIAL_RULES**: レスポンシブ対応・PWA対応

### 🔄 フェーズ定義（Web App特化）
| フェーズ | Webアプリでの内容 | 具体例 |
|----------|------------------|--------|
| 01_DISCOVERY | ユーザー要件・UX目標 | 「ターゲットユーザーは？」 |
| 02_ANALYSIS | 機能分解・ユーザーフロー | 「最適なユーザー体験は？」 |
| 03_ARCHITECTURE | フロント・バック設計 | 「スケーラブルな構成は？」 |
| 04_INTERFACE | API・コンポーネント設計 | 「再利用可能なUIは？」 |
| 05_IMPLEMENTATION | フロント・バック実装 | 「高品質なコードは？」 |
| 06_VALIDATION | E2E・パフォーマンステスト | 「ユーザー要件満足は？」 |
| 07_EXTENSION | PWA・多言語・分析機能 | 「付加価値機能は？」 |

## PROJECT_CONFIG_BLOCK_END
```

---

## 📋 **Template 3: データ分析システム**

```markdown
## PROJECT_CONFIG_BLOCK_START

### 🎯 プロジェクト基本情報
- **PROJECT_NAME**: advanced_data_analytics_platform
- **PROJECT_TYPE**: Data Analysis & Visualization System
- **CURRENT_PHASE**: <phase:02_ANALYSIS>
- **TARGET_GOALS**: 高速分析・直感的可視化・自動レポート生成

### 🔧 技術スタック
- **LANGUAGE**: Python・R・SQL
- **DATABASE**: PostgreSQL・ClickHouse（分析用）
- **ANALYTICS**: pandas・NumPy・SciPy・Plotly・Dash
- **PROCESSING**: Apache Airflow・Celery（並列処理）
- **TOOLS**: Jupyter・DuckDB・Streamlit

### 📊 品質基準
- **PERFORMANCE_TARGET**: <10s大容量データ処理・<3sダッシュボード更新
- **ACCURACY_TARGET**: 統計的有意性p<0.05・信頼区間95%
- **QUALITY_REQUIREMENTS**: データ整合性100%・可視化レスポンス95%
- **SPECIAL_RULES**: 統計的妥当性・データプライバシー保護

### 🔄 フェーズ定義（データ分析特化）
| フェーズ | データ分析での内容 | 具体例 |
|----------|-------------------|--------|
| 01_DISCOVERY | 分析要件・KPI定義 | 「解決すべき課題は？」 |
| 02_ANALYSIS | データ探索・統計分析 | 「データの特徴・傾向は？」 |
| 03_ARCHITECTURE | ETL・分析基盤設計 | 「スケーラブルな分析環境は？」 |
| 04_INTERFACE | ダッシュボード・レポート設計 | 「直感的な可視化は？」 |
| 05_IMPLEMENTATION | 分析・可視化実装 | 「高精度な分析結果は？」 |
| 06_VALIDATION | 統計検証・結果妥当性 | 「分析結果は信頼できるか？」 |
| 07_EXTENSION | 予測分析・AI活用 | 「高度な洞察は？」 |

## PROJECT_CONFIG_BLOCK_END
```

---

## 📋 **Template 4: モバイルアプリケーション**

```markdown
## PROJECT_CONFIG_BLOCK_START

### 🎯 プロジェクト基本情報
- **PROJECT_NAME**: cross_platform_mobile_app
- **PROJECT_TYPE**: Mobile Application
- **CURRENT_PHASE**: <phase:04_INTERFACE>
- **TARGET_GOALS**: 直感的UX・高性能・マルチプラットフォーム対応

### 🔧 技術スタック
- **LANGUAGE**: Dart・Swift・Kotlin
- **FRAMEWORK**: Flutter・React Native
- **DATABASE**: SQLite・Firebase・Realm
- **BACKEND**: Node.js・Express・Socket.io
- **TOOLS**: Xcode・Android Studio・Firebase Analytics

### 📊 品質基準
- **PERFORMANCE_TARGET**: <3s起動時間・60fps維持
- **UX_TARGET**: App Store評価4.5+・離脱率<20%
- **QUALITY_REQUIREMENTS**: クラッシュ率<0.1%・レビュー対応100%
- **SPECIAL_RULES**: プラットフォーム最適化・プライバシー準拠

## PROJECT_CONFIG_BLOCK_END
```

---

## 📋 **Template 5: API・マイクロサービス**

```markdown
## PROJECT_CONFIG_BLOCK_START

### 🎯 プロジェクト基本情報
- **PROJECT_NAME**: scalable_api_microservices
- **PROJECT_TYPE**: API & Microservices
- **CURRENT_PHASE**: <phase:05_IMPLEMENTATION>
- **TARGET_GOALS**: 高可用性・スケーラビリティ・セキュリティ

### 🔧 技術スタック
- **LANGUAGE**: Go・Python・Node.js
- **DATABASE**: PostgreSQL・Redis・MongoDB
- **INFRASTRUCTURE**: Docker・Kubernetes・AWS/GCP
- **API**: GraphQL・REST・gRPC
- **TOOLS**: Terraform・Jenkins・Prometheus

### 📊 品質基準
- **PERFORMANCE_TARGET**: <100ms応答・99.9%可用性
- **SCALABILITY_TARGET**: 10,000 RPS対応・自動スケーリング
- **QUALITY_REQUIREMENTS**: テストカバレッジ90%・セキュリティ監査合格
- **SPECIAL_RULES**: サービス分離・障害隔離・監視徹底

## PROJECT_CONFIG_BLOCK_END
```

---

## 🔧 **カスタマイズガイド**

### **📋 Template選択基準**
1. **AI/ML System**: 予測・分析・学習機能が中心
2. **Web Application**: ユーザー向けWebサービス
3. **Data Analytics**: データ処理・可視化・レポート
4. **Mobile App**: iOS/Android向けアプリケーション
5. **API/Microservices**: バックエンドAPI・サービス基盤

### **⚡ カスタマイズ手順**
1. **適切なTemplateを選択**
2. **PROJECT_CONFIG_BLOCK内の値を更新**
3. **プロジェクト固有要素を追加**
4. **Universal Frameworkと組み合わせ**

### **✅ 設定確認項目**
- [ ] PROJECT_NAME: プロジェクト名の設定
- [ ] CURRENT_PHASE: 現在フェーズの正確な設定
- [ ] TARGET_GOALS: 具体的・測定可能な目標
- [ ] 技術スタック: 実際に使用する技術の明記
- [ ] 品質基準: 数値化された具体的基準

---

**これらのTemplateにより、プロジェクトタイプに応じた最適な設定を迅速に構築できます。** 🎯