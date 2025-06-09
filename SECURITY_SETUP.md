# 🔒 CompanyGenius セキュリティ設定ガイド

## 📋 環境変数の設定

### 必須環境変数

プロジェクト実行前に以下の環境変数を設定してください：

```bash
# データベースパス（必須）
export DATABASE_PATH="/path/to/your/corporate_phase2_stable.db"

# APIキー（必要に応じて）
export BRAVE_API_KEY="your_new_brave_api_key"
export EVERART_API_KEY="your_new_everart_api_key"
export REPLICATE_API_TOKEN="your_new_replicate_token"
```

### APIキーの取得方法

1. **Brave Search API**
   - https://api.search.brave.com/
   - アカウント作成 → API キー発行

2. **EverArt API**
   - https://everart.ai/api
   - アカウント作成 → API トークン取得

3. **Replicate API**
   - https://replicate.com/account/api-tokens
   - アカウント作成 → トークン生成

## 🗃️ データベース設定

### 1. 法人番号データベースの準備

```bash
# データディレクトリ作成
mkdir -p ./data

# 法人番号データベースファイルを配置
# corporate_phase2_stable.db を ./data/ フォルダに配置してください
```

### 2. 環境変数でのパス指定

```bash
# 絶対パス指定
export DATABASE_PATH="/absolute/path/to/corporate_phase2_stable.db"

# 相対パス指定（プロジェクトディレクトリから）
export DATABASE_PATH="./data/corporate_phase2_stable.db"
```

## 🔑 MCP設定ファイル

### `.mcp.json.template` の使用

```bash
# テンプレートをコピー
cp .mcp.json.template .mcp.json

# APIキーを設定
nano .mcp.json
```

### `.mcp.json` の設定例

```json
{
  "mcpServers": {
    "braveSearch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    },
    "everart": {
      "command": "npx", 
      "args": ["-y", "@modelcontextprotocol/server-everart"],
      "env": {
        "EVERART_API_KEY": "${EVERART_API_KEY}"
      }
    },
    "replicate": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-replicate"], 
      "env": {
        "REPLICATE_API_TOKEN": "${REPLICATE_API_TOKEN}"
      }
    }
  }
}
```

## ⚠️ セキュリティ注意事項

### 絶対にコミットしてはいけないファイル

- `.mcp.json` （APIキー含有）
- `*.log` ファイル（個人データ含有可能性）
- `corrections.log` （ユーザーデータ）
- 個人パスを含むファイル

### .gitignore確認

以下が `.gitignore` に含まれていることを確認：

```gitignore
# Security - API Keys and Personal Data
.mcp.json
*.log
corrections.log
server.log
debug_*.log

# Personal environment data
**/Users/*/
**/Desktop/**
```

## 🛠️ トラブルシューティング

### APIキー関連エラー

```bash
# エラー: Invalid API key
# 解決: 環境変数を確認
echo $BRAVE_API_KEY

# 空の場合は再設定
export BRAVE_API_KEY="your_correct_api_key"
```

### データベース接続エラー

```bash
# エラー: Database not found
# 解決: パスを確認
echo $DATABASE_PATH
ls -la "$DATABASE_PATH"

# ファイルが存在しない場合
export DATABASE_PATH="./data/corporate_phase2_stable.db"
```

## 📊 監査チェックリスト

### 定期確認項目

- [ ] APIキーが平文で保存されていない
- [ ] ログファイルが Git 管理下にない
- [ ] 個人パスが除去されている
- [ ] 環境変数が正しく設定されている
- [ ] `.gitignore` が適切に設定されている

### 緊急時対応

APIキー漏洩の疑いがある場合：

1. **即座にAPIキーを無効化**
2. **新しいAPIキーを生成**
3. **Git履歴をクリーンアップ**
4. **環境変数を更新**

---

**⚠️ 重要**: セキュリティは継続的なプロセスです。定期的に設定を見直し、最新のベストプラクティスに従ってください。