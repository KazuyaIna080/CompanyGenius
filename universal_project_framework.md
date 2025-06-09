# 🎯 Universal Project Framework v1.0
## Claude Desktop + MCP環境での高品質プロジェクト開発フレームワーク

---

## 📋 **基本開発方針（全プロジェクト共通）**

### **🎯 本質機能優先戦略**
- **本質・原理・構造を優先**して検討する
- **応用や表面的なコード生成は後回し**にする（必要に応じてのみ）
- 検討の目的・設計意図を**明示的に整理しながら進行する**
- トークンの使い切りや文脈消失に備え、**記録と再利用可能な構成を心がける**

### **📊 段階的実装方針**
- **本質機能**: 仕様 → 設計 → コードの順で進める
- **UI/UX開発**: 機能確認・要件整理が完了した段階で着手する
- **類似コード回避**: 毎回設計理由を問い直すようにする
- **品質保証**: 各段階での品質ゲート実行

---

## 🔄 **Phase-Q Template準拠（7段階フェーズ）**

### **📋 共通フェーズ定義**
| フェーズ | 内容 | 共通質問例 | 成果物例 |
|----------|------|-----------|----------|
| **01_DISCOVERY** | 目的・課題発見 | 「なぜこれが必要か？」 | requirements.md |
| **02_ANALYSIS** | 要件・機能分解 | 「成功を計測する指標は？」 | feature_spec.md |
| **03_ARCHITECTURE** | 構造・データ設計 | 「最適なアーキテクチャは？」 | architecture.drawio |
| **04_INTERFACE** | API・I/F設計 | 「外部との契約は？」 | api_design.yaml |
| **05_IMPLEMENTATION** | コーディング | 「設計意図に沿った実装は？」 | source_code/ |
| **06_VALIDATION** | テスト・本質確認 | 「目的指標を満たすか？」 | test_results.json |
| **07_EXTENSION** | 応用・拡張 | 「本質を壊さずに拡張できるか？」 | extensions/ |

### **🔄 フェーズ進行ルール**
- フェーズ進展前に**批評家エージェント**で方向性確認
- 各フェーズ完了時に**進行記録**を作成
- **Phase-Q Template**の対応する質問を必ず検討
- 本質確認なしの応用・拡張は保留

---

## 🔧 **品質管理システム（全プロジェクト共通）**

### **✅ 必須品質基準**
- **エラー0%**: 全段階でエラー発生を許可しない
- **文字コード統一**: UTF-8完全統一・文字化け0%
- **動作確認**: Windows環境での完璧動作保証
- **再現性**: 他環境での確実な再現可能性

### **🔍 品質ゲートシステム**
```python
# 共通品質チェック関数
def universal_quality_gate(project_metrics, phase_requirements):
    """全プロジェクト共通の品質ゲート"""
    basic_requirements = {
        'error_rate': project_metrics.get('error_rate', 1.0) == 0.0,
        'charset_quality': project_metrics.get('charset_errors', 1) == 0,
        'documentation': project_metrics.get('doc_coverage', 0) >= 0.8,
        'test_coverage': project_metrics.get('test_coverage', 0) >= 0.7
    }
    
    phase_specific = all(
        project_metrics.get(key, 0) >= threshold 
        for key, threshold in phase_requirements.items()
    )
    
    return all(basic_requirements.values()) and phase_specific
```

### **📊 文字コード品質管理（必須）**
```python
# プロジェクト開始時の必須セットアップ
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

def project_charset_setup():
    """全プロジェクト共通: 文字コード環境設定"""
    # Windows環境最適化
    if os.name == 'nt':
        os.system('chcp 65001')  # UTF-8コードページ
    
    # pandas設定
    import pandas as pd
    pd.set_option('display.unicode.east_asian_width', True)
    
    print("文字コード環境設定完了")

def project_data_checkpoint(df, stage_name, artifact_id=None):
    """全プロジェクト共通: データ品質チェックポイント"""
    # 文字化けチェック
    charset_issues = 0
    for col in df.select_dtypes(include=['object']).columns:
        issues = df[col].str.contains(r'[竄｢｣､ܗ튔]', regex=True, na=False).sum()
        charset_issues += issues
    
    quality_passed = charset_issues == 0
    
    if not quality_passed:
        raise ValueError(f"文字コード品質問題: {charset_issues}件検出")
    
    print(f"✅ {stage_name} 品質チェック: 合格")
    return quality_passed
```

---

## 🚀 **Claude Desktop + MCP活用方針**

### **🔧 推奨MCP拡張機能**
- **filesystem**: 大容量ファイル操作・ログ管理
- **sequential-thinking**: 複雑問題の段階的解決
- **memory**: プロジェクト履歴・設定保存
- **brave_web_search**: 最新技術情報・競合調査

### **⚡ 開発効率化ルール**
- **50行制限**: ファイル分割での最適実装
- **Unicode注意**: 絵文字・特殊文字の適切処理
- **コメント確認**: #コメントの取り忘れ防止
- **Windows最適化**: 環境固有問題の事前対策

---

## 📝 **進行記録システム（全プロジェクト共通）**

### **📋 標準進行記録テンプレート**
```markdown
## 《進行記録》<phase:XX_PHASE_NAME> 完了

### 📊 **達成成果**
- **主要成果**: [具体的な成果物]
- **品質指標**: [エラー率・精度・性能等]
- **技術資産**: [新規作成・更新されたファイル]

### 🔧 **技術決定事項**
- **アーキテクチャ**: [設計決定とその理由]
- **技術選択**: [選択した技術・ライブラリとその根拠]
- **品質基準**: [設定した品質基準・閾値]

### 🎯 **次Phase目標**
- **主目標**: [次段階の具体的目標]
- **技術課題**: [解決すべき技術的課題]
- **品質要求**: [達成すべき品質基準]

### ⚠️ **注意事項・リスク**
- **技術リスク**: [予想される技術的リスク]
- **品質リスク**: [品質劣化の可能性]
- **スケジュールリスク**: [遅延要因]

### 📅 **更新日時**: 2025-XX-XX
### 👤 **記録者**: Claude Sonnet 4
```

### **🔄 チェックポイントシステム**
- **Phase完了時**: 必須進行記録作成
- **週次**: プロジェクト状況確認
- **月次**: 品質指標レビュー
- **緊急時**: 問題発生時の即座記録

---

## 🧠 **批評家エージェント（全プロジェクト共通）**

### **🔍 必須確認項目**
- **🎯 本来の目的**: 話が逸れていないか？
- **🔁 繰り返し回避**: 同じやり取りを繰り返していないか？
- **🧩 前提確認**: 忘れている合意がないか？
- **💭 思考確認**: 必要な検討が抜けていないか？

### **⚠️ 共通暴走パターン**
- **早期実装**: 本質確認不十分での具体実装
- **応用脱線**: 基盤完成前の応用アイデア追求
- **品質妥協**: エラー許容・文字化け放置
- **文脈消失**: トークン消費による設計意図忘却

---

## 🎯 **プロジェクト設定カスタマイズポイント**

### **📋 設定必須項目（プロジェクト固有）**
```markdown
## PROJECT_CONFIG_BLOCK_START

### 🎯 プロジェクト基本情報
- **PROJECT_NAME**: [プロジェクト名]
- **PROJECT_TYPE**: [Web App / Data Analysis / AI/ML System / etc.]
- **CURRENT_PHASE**: [現在のフェーズ]
- **TARGET_GOALS**: [具体的目標・KPI]

### 🔧 技術スタック
- **LANGUAGE**: [Python / JavaScript / etc.]
- **DATABASE**: [SQLite / PostgreSQL / MongoDB / etc.]
- **FRAMEWORK**: [FastAPI / React / Django / etc.]
- **TOOLS**: [特殊ツール・ライブラリ]

### 📊 品質基準
- **PERFORMANCE_TARGET**: [応答時間・処理速度目標]
- **ACCURACY_TARGET**: [精度・正確性目標]
- **QUALITY_REQUIREMENTS**: [エラー率・可用性目標]
- **SPECIAL_RULES**: [プロジェクト固有ルール]

## PROJECT_CONFIG_BLOCK_END
```

### **🔄 カスタマイズ手順**
1. **PROJECT_CONFIG_BLOCK**内の設定値を更新
2. **フェーズ定義**をプロジェクトタイプに応じて調整
3. **成果物構成**をドメインに合わせて設計
4. **固有ルール**を必要に応じて追加

---

## 📁 **標準ファイル構成テンプレート**

```
{PROJECT_NAME}/
├── 01_project_overview.md          # プロジェクト全体像
├── 02_feature_spec.md              # 機能仕様
├── 03_architecture.drawio          # システム設計
├── 04_api_design.yaml              # API仕様
├── 05_implementation/              # 実装ファイル
│
├── quality_assurance/              # 品質保証
│   ├── test_results.json
│   ├── performance_benchmarks.csv
│   └── quality_reports/
│
├── documentation/                  # ドキュメント
│   ├── user_guide.md
│   ├── api_reference.md
│   └── deployment_guide.md
│
├── logs/                          # 進行ログ
│   ├── phase_progress_records/
│   ├── quality_checkpoints/
│   └── issue_resolution_logs/
│
└── deployment/                    # 展開準備
    ├── configuration/
    ├── scripts/
    └── monitoring/
```

---

## ✅ **フレームワーク適用チェックリスト**

### **🚀 プロジェクト開始時**
- [ ] PROJECT_CONFIG_BLOCKの設定完了
- [ ] 文字コード環境セットアップ実行
- [ ] Phase-Q Template準拠確認
- [ ] 品質ゲート基準設定

### **📊 各Phase完了時**
- [ ] 品質ゲート実行・合格確認
- [ ] 進行記録作成・保存
- [ ] 批評家エージェントによる方向性確認
- [ ] 次Phase準備・目標設定

### **🔧 継続的品質管理**
- [ ] エラー0%維持確認
- [ ] 文字コード品質維持
- [ ] ドキュメント更新
- [ ] バックアップ・バージョン管理

---

---

## 🔒 **GitHub公開前必須セキュリティ・コンプライアンス監査**

### **⚠️ 全GitHub公開プロジェクトに強制適用**

#### **💡 適用ルール**
- **例外なし**: すべてのパブリックリポジトリに適用
- **実行タイミング**: 初回コミット前・公開前
- **詳細手順**: `GITHUB_SECURITY_RULES.md` 参照

#### **🔍 必須チェック項目**

**1. セキュリティ監査**
- [ ] APIキー・認証情報の完全除去
- [ ] 個人情報・個人パスの匿名化
- [ ] ログファイル・実データの除外  
- [ ] 環境変数化の実装
- [ ] .gitignore・セキュリティ文書の整備

**2. コンプライアンス確認**
- [ ] データソース利用規約の検証
- [ ] 商用利用可否の確認
- [ ] 必要なアトリビューション記載
- [ ] ライセンス互換性確認
- [ ] 準拠性文書の作成

#### **📋 チェック実行手順**
```bash
# 1. 自動スキャン実行
grep -r "api_key\|password\|token" --exclude-dir=.git .
grep -r "/Users/\|/home/[^/]*/" --exclude-dir=.git .
find . -name "*.log" -o -name "*.env" | grep -v template

# 2. 手動確認
# 全ファイルの目視確認（設定ファイル、コメント等）

# 3. データソース確認
# 利用API・データベースの利用規約確認
```

#### **🚨 違反時の対応**
1. **リポジトリ即座プライベート化**
2. **問題ファイル特定・除去**
3. **APIキー等無効化・再生成**
4. **修正完了後の再監査**

**⚠️ ゼロトレランス**: セキュリティ・コンプライアンス違反は一切許可されません

---

**このUniversal Frameworkにより、セキュリティ・コンプライアンスを保ちながら高品質・高効率な開発を実現できます。** 🎯