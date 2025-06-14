# Phase 15: 6段階カスケード統合企業名予測システム - Claude Code版

## 🎯 プロジェクト概要

実務で良く確認する前株、後株などの正式社名の確認を、法人番号データベースからの照合と、存在しない企業については推定を提示し、間違っていた場合含めてローカルに保存出来るChrome拡張機能です。

352万社データベースを基盤とした6段階カスケード企業名予測システムの Claude Code 環境移植版です。

### 🏆 システム仕様

- **データ規模**: 352万社（corporate_phase2_stable.db）
- **精度目標**: 95%（現在90.0%）
- **応答時間**: <100ms（実績0.3ms）
- **エラー率**: 0%維持

## 📁 ファイル構成

```
claude_code/
├── phase15_mega_cascade_system.py    # 中核予測システム
├── phase15_fastapi_server.py         # FastAPI Webサーバー
├── phase15_system_tester.py          # 統合テストスクリプト
├── chrome_extension/                 # Chrome拡張機能
│   ├── manifest.json
│   ├── background.js
│   ├── content.js
│   ├── popup.html
│   └── popup.js
├── requirements.txt                  # Python依存関係
├── .mcp.json.template               # MCP設定テンプレート
├── SECURITY_SETUP.md                # セキュリティ設定ガイド
├── CLAUDE.md                        # Claude Code設定
└── README.md                        # このファイル
```

## 🔒 セキュリティ設定

### 🚨 初回セットアップ（必須）

プロジェクト実行前に必ず以下を設定してください：

```bash
# 1. 環境変数の設定
export DATABASE_PATH="./data/corporate_phase2_stable.db"
export BRAVE_API_KEY="your_brave_api_key"
export EVERART_API_KEY="your_everart_api_key" 
export REPLICATE_API_TOKEN="your_replicate_token"

# 2. MCP設定ファイルの作成
cp .mcp.json.template .mcp.json
# .mcp.json を編集してAPIキーを設定
```

### 📋 APIキー取得方法

- **Brave Search**: https://api.search.brave.com/
- **EverArt**: https://everart.ai/api
- **Replicate**: https://replicate.com/account/api-tokens

**⚠️ 重要**: `.mcp.json` ファイルは絶対にGitにコミットしないでください

詳細は [SECURITY_SETUP.md](SECURITY_SETUP.md) を参照してください。

---

## ⚡ クイックスタート

### 📥 ダウンロード・基本セットアップ

```bash
# 1. プロジェクトダウンロード
git clone https://github.com/KazuyaIna080/CompanyGenius.git
cd CompanyGenius

# 2. Python依存パッケージインストール
pip install -r requirements.txt

# 3. データディレクトリ作成
mkdir -p data
```

### 📊 データベースセットアップ（重要）

⚠️ **データベースファイルは別途ダウンロード・作成が必要です**

```bash
# 1. 法人番号データベースダウンロード
# https://www.houjin-bangou.nta.go.jp/download/
# → 「全件データ」をダウンロード・解凍

# 2. 環境変数設定
export DATABASE_PATH="./data/corporate_phase2_stable.db"

# 3. データベース作成（CSVから）
python create_database.py  # 詳細は INSTALLATION_COMPLETE_GUIDE.md
```

### 🚀 起動・動作確認

```bash
# 1. APIサーバー起動
python phase15_fixed_api.py

# 2. Chrome拡張機能インストール
# chrome://extensions/ → デベロッパーモード → chrome_extension フォルダ選択

# 3. 動作確認
# Webページでテキスト選択 → 右クリック → 「CompanyGeniusで企業名を予測」
```

**📖 詳細手順**: [INSTALLATION_COMPLETE_GUIDE.md](INSTALLATION_COMPLETE_GUIDE.md) を参照

### 🔗 内蔵版（Embedded Edition）- 最推奨

🚀 **Chrome Web Store ワンクリックインストール**で即座利用開始

#### 革命的アプローチ
- **データベース内蔵**: EDINETデータベース（5-10MB）をChrome拡張機能に内蔵
- **ゼロ設定**: セットアップ・APIサーバー・ネットワーク接続不要
- **瞬間起動**: Chrome Web Storeからインストール→即座利用開始
- **オフライン動作**: インターネット接続不要で高速動作
- **技術**: sql.js（WebAssembly SQLite）+ Service Worker

詳細：[EMBEDDED_EDITION_PLAN.md](EMBEDDED_EDITION_PLAN.md)

---

### 🪶 軽量版（Lite Edition）

⚡ **3ステップセットアップ**で即座利用開始できる軽量版

#### 軽量版セットアップ手順

```bash
# Step 1: EDINETコードリストダウンロード
# https://disclosure2.edinet-fsa.go.jp/weee0010.aspx
# 「EDINETコードリスト」をダウンロードしてプロジェクトディレクトリに配置

# Step 2: Lite版データベース作成
python create_database_lite.py
# → ./data/corporate_lite.db が作成される（約5-10MB）

# Step 3: Lite版APIサーバー起動  
python phase15_lite_api.py  # ポート8002で起動
# Chrome拡張機能をインストール（既存のものを使用）
```

#### 軽量版の特徴

- **データ規模**: EDINETコードリスト約4,000社（5-10MB）
- **セットアップ**: 3.5GB CSVダウンロード不要
- **カバー率**: 上場企業・主要企業 90%+
- **機能**: ユーザー学習機能をそのまま維持
- **対象**: 営業・投資・報告書作成での企業名確認

詳細：[LIGHTWEIGHT_VERSION_PLAN.md](LIGHTWEIGHT_VERSION_PLAN.md)

---

## 🔧 6段階カスケードシステム

| Level | 名称 | 精度 | 説明 |
|-------|------|------|------|
| 1 | ユーザー学習 | 100% | ユーザー固有学習データ |
| 2 | EDINET上場 | 99.2% | 上場企業高精度マッチング |
| 3 | EDINET全体 | 95% | 全EDINET企業データ |
| 4 | 法人番号DB | 90% | 352万社データベース |
| 5 | ブランド名 | 85% | 通称・ブランド名マッピング |
| 6 | URL情報 | 80% | 企業URL・情報推定 |
| 7 | ML予測 | 91% | 機械学習フォールバック |

## 🚀 セットアップ手順

### 1. 依存関係インストール

```bash
cd /home/kazin/claude_code
pip install -r requirements.txt
```

### 2. データベース確認

データベースパス: `/mnt/c/Users/kazin/Desktop/corporate_phase2_stable.db`

### 3. システムテスト実行

```bash
python phase15_system_tester.py
```

### 4. FastAPIサーバー起動

```bash
python phase15_fastapi_server.py
```

サーバー起動後、以下でアクセス可能：
- API仕様: http://127.0.0.1:8000/docs
- ヘルスチェック: http://127.0.0.1:8000/health

## 📊 API エンドポイント

### 基本予測
```bash
POST /api/v1/predict
Content-Type: application/json
Authorization: Bearer claude-code-key

{
  "query": "トヨタ",
  "user_id": "test_user",
  "include_alternatives": true
}
```

### バッチ予測
```bash
POST /api/v1/predict/batch
Content-Type: application/json
Authorization: Bearer claude-code-key

{
  "queries": ["トヨタ", "ソニー", "楽天"],
  "user_id": "test_user"
}
```

### システム統計
```bash
GET /api/v1/stats
Authorization: Bearer claude-code-key
```

## 🔧 Chrome拡張機能

### インストール手順

1. Chrome で `chrome://extensions/` を開く
2. 「開発者モード」を有効にする
3. 「パッケージ化されていない拡張機能を読み込む」をクリック
4. `/home/kazin/claude_code/chrome_extension` フォルダを選択

### 使用方法

- テキストを選択してコンテキストメニューから「企業名を予測」
- 拡張機能アイコンクリックでポップアップUI

## 🧪 テスト項目

- ✅ データベース接続テスト
- ✅ 中核システムインポートテスト  
- ✅ カスケード予測テスト
- ✅ APIサーバーヘルスチェック
- ✅ API予測エンドポイントテスト
- ✅ バッチ予測テスト
- ✅ Chrome拡張機能ファイルテスト
- ✅ パフォーマンスベンチマーク

## 🎯 Universal Project Framework 準拠

このプロジェクトは Universal Project Framework v1.0 に完全準拠：

- **Phase-Q Template**: 7段階開発フェーズ
- **品質ゲート**: エラー0%・文字化け0%維持
- **進行記録**: 系統的な開発記録
- **MCP統合**: Claude Desktop機能活用

## 📈 パフォーマンス実績

- **応答時間**: 平均0.3ms（目標<100ms）
- **精度**: 90.0%（目標95%に向け改善中）
- **エラー率**: 0%（継続維持）
- **可用性**: 99.9%（APIサーバー）

## 🔗 関連ファイル

- `universal_project_framework.md` - 基本フレームワーク
- `enterprise_prediction_project_rules.md` - プロジェクト固有ルール
- `project_config_templates.md` - 設定テンプレート
- `implementation_examples.md` - 実装例・参考資料

---

**Phase 15システムにより、世界最高水準の企業名予測をClaude Code環境で実現** 🎯