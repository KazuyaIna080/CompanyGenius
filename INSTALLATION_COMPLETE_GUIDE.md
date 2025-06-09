# 🚀 CompanyGenius 完全インストールガイド

## 📋 システム要件

- **OS**: Windows 10/11, macOS, Linux
- **Python**: 3.8以上
- **Chrome**: 最新版
- **ディスク容量**: 4GB以上（データベース用）
- **メモリ**: 4GB以上推奨

---

## 🔧 Step 1: プロジェクトダウンロード

### GitHub からダウンロード

```bash
# 方法A: Git clone
git clone https://github.com/KazuyaIna080/CompanyGenius.git
cd CompanyGenius

# 方法B: ZIP ダウンロード
# 1. https://github.com/KazuyaIna080/CompanyGenius
# 2. 緑色の「Code」ボタン → 「Download ZIP」
# 3. 解凍してフォルダに移動
```

---

## 📊 Step 2: データベースセットアップ（重要）

### 2-1: データディレクトリ作成

```bash
mkdir -p data
```

### 2-2: 法人番号データベースダウンロード

#### **Option A: 国税庁から直接ダウンロード（推奨）**

```bash
# 1. 法人番号公表サイトにアクセス
# https://www.houjin-bangou.nta.go.jp/download/

# 2. 「全件データ」をダウンロード
# ファイル名例: 01_houjin_all_20241201.zip (約1.2GB)

# 3. 解凍
unzip 01_houjin_all_20241201.zip

# 4. CSVファイルを確認
ls -la *.csv
# 出力例: 01_houjin_all_20241201.csv (約3.5GB)
```

#### **Option B: SQLiteデータベース作成**

```python
# create_database.py を作成
import sqlite3
import csv
import os

def create_corporate_database():
    """法人番号CSVからSQLiteデータベースを作成"""
    
    # CSVファイルのパスを確認
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'houjin' in f]
    if not csv_files:
        print("❌ 法人番号CSVファイルが見つかりません")
        print("https://www.houjin-bangou.nta.go.jp/download/ からダウンロードしてください")
        return
    
    csv_file = csv_files[0]
    db_path = './data/corporate_phase2_stable.db'
    
    print(f"📊 CSVファイル: {csv_file}")
    print(f"📁 データベース: {db_path}")
    
    # SQLiteデータベース作成
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # テーブル作成
    cursor.execute('''
        CREATE TABLE companies (
            id INTEGER PRIMARY KEY,
            corporate_number TEXT,
            company_name TEXT,
            company_name_kana TEXT,
            address TEXT,
            prefecture_code TEXT,
            city_code TEXT,
            street_address TEXT,
            phone TEXT,
            establishment_date TEXT,
            capital TEXT,
            employee_count TEXT,
            business_category TEXT,
            status TEXT
        )
    ''')
    
    # CSVデータ読み込み
    print("📥 CSVデータ読み込み中...")
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # ヘッダーをスキップ
        
        batch_size = 10000
        batch_data = []
        count = 0
        
        for row in reader:
            # データをバッチに追加
            batch_data.append(row[:14])  # 最初の14列を使用
            count += 1
            
            # バッチサイズに達したらデータベースに挿入
            if len(batch_data) >= batch_size:
                cursor.executemany('''
                    INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', batch_data)
                conn.commit()
                batch_data = []
                print(f"  📈 {count:,} 件処理完了")
        
        # 残りのデータを挿入
        if batch_data:
            cursor.executemany('''
                INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', batch_data)
            conn.commit()
    
    # インデックス作成（検索高速化）
    print("🔍 インデックス作成中...")
    cursor.execute('CREATE INDEX idx_company_name ON companies(company_name)')
    cursor.execute('CREATE INDEX idx_corporate_number ON companies(corporate_number)')
    
    conn.close()
    
    print(f"✅ データベース作成完了: {db_path}")
    print(f"📊 総レコード数: {count:,} 件")

if __name__ == "__main__":
    create_corporate_database()
```

```bash
# データベース作成実行
python create_database.py
```

### 2-3: データベース確認

```bash
# データベースファイルの確認
ls -la data/corporate_phase2_stable.db

# サイズ確認（約1-2GB程度）
du -h data/corporate_phase2_stable.db
```

---

## 🔑 Step 3: 環境変数設定

### 3-1: 設定ファイル作成

```bash
# MCP設定ファイル作成
cp .mcp.json.template .mcp.json

# 環境変数設定
export DATABASE_PATH="./data/corporate_phase2_stable.db"
```

### 3-2: APIキー設定（オプション）

#### 必要なAPIキー（機能拡張用）

1. **Brave Search API** (Web検索機能)
   - https://api.search.brave.com/
   - アカウント作成 → APIキー取得

2. **EverArt API** (画像生成機能)
   - https://everart.ai/api
   - APIトークン取得

3. **Replicate API** (AI機能拡張)
   - https://replicate.com/account/api-tokens
   - トークン生成

#### APIキー設定

```bash
# 環境変数として設定
export BRAVE_API_KEY="your_brave_api_key"
export EVERART_API_KEY="your_everart_api_key"
export REPLICATE_API_TOKEN="your_replicate_token"

# .mcp.json ファイルを編集してAPIキーを記載
nano .mcp.json
```

---

## 🐍 Step 4: Python環境セットアップ

### 4-1: 依存パッケージインストール

```bash
# Python依存パッケージインストール
pip install -r requirements.txt

# または個別インストール
pip install sqlite3 fastapi uvicorn requests beautifulsoup4 lxml
```

### 4-2: 動作確認

```bash
# APIサーバー起動テスト
python phase15_fixed_api.py

# 別ターミナルでテスト
curl http://localhost:8001/predict -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "トヨタ"}'

# 期待する結果例:
# {"prediction": "トヨタ自動車株式会社", "confidence": 0.95}
```

---

## 🔧 Step 5: Chrome拡張機能インストール

### 5-1: 開発者モードでインストール

```bash
# 1. Chrome を開く
# 2. アドレスバーに入力: chrome://extensions/
# 3. 右上の「デベロッパーモード」をオンにする
# 4. 「パッケージ化されていない拡張機能を読み込む」をクリック
# 5. プロジェクトの「chrome_extension」フォルダを選択
# 6. CompanyGenius拡張機能が追加されることを確認
```

### 5-2: 動作確認

```bash
# 1. APIサーバーが起動していることを確認
python phase15_fixed_api.py

# 2. Chromeで任意のWebサイトを開く
# 3. テキストを選択して右クリック
# 4. 「CompanyGeniusで企業名を予測」を選択
# 5. 予測結果ダイアログが表示されることを確認
```

---

## 🔍 Step 6: トラブルシューティング

### データベース関連

```bash
# エラー: Database not found
echo $DATABASE_PATH
ls -la "$DATABASE_PATH"

# 解決: パスを確認・修正
export DATABASE_PATH="./data/corporate_phase2_stable.db"
```

### APIサーバー関連

```bash
# エラー: Port already in use
# 解決: ポート変更またはプロセス終了
lsof -i :8001
kill -9 [PID]

# または別ポートで起動
python phase15_fixed_api.py --port 8002
```

### Chrome拡張機能関連

```bash
# エラー: Extension not loading
# 解決:
# 1. manifest.json の文法確認
# 2. chrome://extensions/ で再読み込み
# 3. ブラウザ再起動
```

---

## 📊 データソース情報

### 利用データ

1. **法人番号公表システム（国税庁）**
   - 出典：国税庁法人番号公表サイト
   - ライセンス：政府標準利用規約（第2.0版）準拠
   - 商用利用：可能
   - データ基準日：2025年6月7日現在
   - データ更新：手動更新（将来的に自動スケジューリング実装予定）

2. **EDINET（金融庁）**
   - 出典：EDINET（金融庁）
   - ライセンス：公共データ利用規約（PDL1.0）準拠
   - 商用利用：可能（出典明記要）

### 注意事項

このサービスは、国税庁法人番号システムWeb-API機能を利用して取得した情報をもとに作成していますが、サービスの内容は国税庁によって保証されたものではありません。

---

## 🎯 使用開始

すべてのセットアップが完了したら：

1. **APIサーバー起動**: `python phase15_fixed_api.py`
2. **Chrome拡張機能**: 右クリックメニューから利用
3. **ポップアップ**: Chrome拡張機能アイコンクリックで利用

**🚀 CompanyGeniusをお楽しみください！**

---

## 📞 サポート

- **GitHub Issues**: https://github.com/KazuyaIna080/CompanyGenius/issues
- **ドキュメント**: README.md、各種ガイドファイル参照
- **セキュリティ**: SECURITY_SETUP.md参照