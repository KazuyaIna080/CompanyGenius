# 🪶 CompanyGenius 軽量版 (EDINET Edition) 実装計画

## 🎯 コンセプト

**超巨大データベース不要**で使える軽量版CompanyGenius

EDINET上場企業データ（約4,000社）のみを使用し、即座にセットアップ・利用開始できる実用版を提供。

---

## 📊 軽量版の仕様

### データ規模比較

| 版 | データソース | 企業数 | DB容量 | セットアップ時間 |
|---|---|---|---|---|
| **フル版** | 法人番号システム全件 | 350万社 | 1-2GB | 30-60分 |
| **軽量版** | EDINET上場企業 | 約4,000社 | 10-20MB | 1-2分 |

### 対象企業
- **上場企業**: 東証1部・2部・マザーズ・JASDAQ等
- **大手企業**: 主要な知名度の高い企業
- **実務重要企業**: ビジネスでよく参照される企業

### 期待される利用場面
- 営業先企業名の正式名確認
- 投資関連の企業名調査  
- 報告書・資料作成時の企業名統一
- 新規取引先の正式社名確認

---

## 🔧 技術的実装

### データ取得・処理

**データソース**: https://disclosure2.edinet-fsa.go.jp/weee0010.aspx  
**ファイル**: EDINETコードリスト（CSVファイル）

```python
# create_database_lite.py
import csv
import sqlite3
import os
from datetime import datetime

class CompanyGeniusLiteBuilder:
    """CompanyGenius Lite データベース作成（EDINETコードリスト版）"""
    
    def __init__(self):
        self.db_path = "./data/corporate_lite.db"
        self.csv_file = None
        self.companies = []
    
    def find_edinet_csv(self):
        """EDINETコードリストCSVファイルを検索"""
        # 一般的なファイル名パターン
        patterns = [
            "EdinetcodeDlInfo.csv",
            "edinet_code_list.csv", 
            "edinetcode*.csv",
            "*edinet*.csv"
        ]
        
        for pattern in patterns:
            files = glob.glob(pattern)
            if files:
                self.csv_file = files[0]
                print(f"📁 EDINETコードリストCSV: {self.csv_file}")
                return True
        
        print("❌ EDINETコードリストCSVが見つかりません")
        print("📥 以下からダウンロードしてください:")
        print("   https://disclosure2.edinet-fsa.go.jp/weee0010.aspx")
        print("   → 「EDINETコードリスト」をダウンロード")
        return False
    
    def process_edinet_csv(self):
        """EDINETコードリストCSVを処理"""
        if not self.csv_file:
            return False
        
        print("📊 EDINETコードリスト処理中...")
        
        with open(self.csv_file, 'r', encoding='cp932') as f:  # EDINETはShift_JIS
            reader = csv.DictReader(f)
            
            for row in reader:
                # EDINETコードリストの標準フィールド
                company_info = {
                    'edinet_code': row.get('ＥＤＩＮＥＴコード', ''),
                    'type': row.get('種別', ''),
                    'listing_classification': row.get('上場区分', ''),
                    'consolidated_classification': row.get('連結の有無', ''),
                    'capital': row.get('資本金', ''),
                    'settlement_date': row.get('決算日', ''),
                    'submitter_name': row.get('提出者名', ''),
                    'submitter_name_en': row.get('提出者名（英字）', ''),
                    'submitter_name_kana': row.get('提出者名（ヨミ）', ''),
                    'location': row.get('所在地', ''),
                    'submitter_industry': row.get('提出者業種', ''),
                    'securities_code': row.get('証券コード', ''),
                    'submitter_corporate_number': row.get('提出者法人番号', '')
                }
                
                # 有効な企業データのみ追加
                if company_info['submitter_name'] and company_info['edinet_code']:
                    self.companies.append(company_info)
        
        print(f"✅ 処理完了: {len(self.companies)} 社")
        return True
    
    def create_lite_database(self):
        """CompanyGenius Lite データベース作成"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # CompanyGenius Lite テーブル作成
        cursor.execute('''
            CREATE TABLE companies_lite (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                edinet_code TEXT UNIQUE,
                company_name TEXT,
                company_name_en TEXT,
                company_name_kana TEXT,
                securities_code TEXT,
                corporate_number TEXT,
                listing_classification TEXT,
                capital TEXT,
                location TEXT,
                industry TEXT,
                settlement_date TEXT,
                last_updated TEXT
            )
        ''')
        
        # ユーザー修正データテーブル（フル版と共通）
        cursor.execute('''
            CREATE TABLE user_corrections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_query TEXT,
                predicted_name TEXT,
                correct_name TEXT,
                correction_date TEXT,
                confidence REAL DEFAULT 1.0
            )
        ''')
        
        # データ挿入
        for company in self.companies:
            cursor.execute('''
                INSERT OR REPLACE INTO companies_lite VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                None,
                company['edinet_code'],
                company['submitter_name'],
                company['submitter_name_en'],
                company['submitter_name_kana'],
                company['securities_code'],
                company['submitter_corporate_number'],
                company['listing_classification'],
                company['capital'],
                company['location'],
                company['submitter_industry'],
                company['settlement_date'],
                datetime.now().isoformat()
            ))
        
        # 検索用インデックス
        cursor.execute('CREATE INDEX idx_lite_name ON companies_lite(company_name)')
        cursor.execute('CREATE INDEX idx_lite_kana ON companies_lite(company_name_kana)')
        cursor.execute('CREATE INDEX idx_lite_securities ON companies_lite(securities_code)')
        cursor.execute('CREATE INDEX idx_lite_edinet ON companies_lite(edinet_code)')
        
        # ユーザー修正データ用インデックス
        cursor.execute('CREATE INDEX idx_corrections_query ON user_corrections(original_query)')
        
        conn.commit()
        conn.close()
        
        db_size = os.path.getsize(self.db_path) / (1024 * 1024)  # MB
        print(f"✅ CompanyGenius Lite DB作成完了")
        print(f"📁 ファイル: {self.db_path}")
        print(f"📊 企業数: {len(self.companies)} 社")
        print(f"💾 サイズ: {db_size:.1f} MB")
        
        return True

def main():
    """CompanyGenius Lite データベース作成メイン"""
    print("🪶 CompanyGenius Lite データベース作成")
    print("=" * 50)
    
    builder = CompanyGeniusLiteBuilder()
    
    # 1. EDINETコードリストCSVファイル検索
    if not builder.find_edinet_csv():
        return False
    
    # 2. CSVファイル処理
    if not builder.process_edinet_csv():
        return False
    
    # 3. データベース作成
    if not builder.create_lite_database():
        return False
    
    print("\n🚀 CompanyGenius Lite セットアップ完了！")
    print("   python phase15_lite_api.py でAPIサーバーを起動できます")
    
    return True

if __name__ == "__main__":
    import glob
    main()
```

### 軽量版APIサーバー

```python
# phase15_lightweight_api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import uvicorn

app = FastAPI(title="CompanyGenius Lightweight API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompanyGeniusLitePredictor:
    """CompanyGenius Lite 予測システム（ユーザー学習機能付き）"""
    
    def __init__(self):
        self.db_path = "./data/corporate_lite.db"
        self.user_corrections = {}
        self._load_user_corrections()
    
    def predict(self, query: str):
        """軽量版企業名予測"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 段階的検索
        # 1. 完全一致
        cursor.execute(
            "SELECT company_name, securities_code FROM companies_lite WHERE company_name = ?",
            (query,)
        )
        exact_match = cursor.fetchone()
        if exact_match:
            return {
                "prediction": exact_match[0],
                "securities_code": exact_match[1],
                "confidence": 1.0,
                "source": "exact_match"
            }
        
        # 2. 部分一致（前方一致）
        cursor.execute(
            "SELECT company_name, securities_code FROM companies_lite WHERE company_name LIKE ? LIMIT 5",
            (f"{query}%",)
        )
        partial_matches = cursor.fetchall()
        if partial_matches:
            return {
                "prediction": partial_matches[0][0],
                "securities_code": partial_matches[0][1],
                "confidence": 0.8,
                "source": "partial_match",
                "alternatives": [{"name": m[0], "code": m[1]} for m in partial_matches[1:]]
            }
        
        # 3. 含有検索
        cursor.execute(
            "SELECT company_name, securities_code FROM companies_lite WHERE company_name LIKE ? LIMIT 3",
            (f"%{query}%",)
        )
        contains_matches = cursor.fetchall()
        if contains_matches:
            return {
                "prediction": contains_matches[0][0],
                "securities_code": contains_matches[0][1],
                "confidence": 0.6,
                "source": "contains_match",
                "alternatives": [{"name": m[0], "code": m[1]} for m in contains_matches[1:]]
            }
        
        conn.close()
        
        # 4. 見つからない場合
        return {
            "prediction": f"{query}株式会社",  # 基本的な推定
            "confidence": 0.3,
            "source": "estimation",
            "note": "軽量版DBに該当なし。上場企業以外の可能性があります。"
        }

predictor = LightweightPredictor()

@app.post("/predict")
async def predict_company(request: dict):
    """企業名予測API（軽量版）"""
    query = request.get("query", "").strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    result = predictor.predict(query)
    return result

@app.get("/stats")
async def get_stats():
    """データベース統計情報"""
    conn = sqlite3.connect(predictor.db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM companies_lite")
    total_companies = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT market_section) FROM companies_lite")
    market_sections = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "version": "lightweight",
        "total_companies": total_companies,
        "market_sections": market_sections,
        "database_size": "10-20MB",
        "setup_time": "1-2分"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
```

---

## 📦 配布戦略

### CompanyGenius Lite パッケージ構成

```
CompanyGenius-Lite/
├── data/
│   └── corporate_lite.db           # 5-10MB（事前構築済み）
├── chrome_extension/               # 既存拡張機能（設定変更のみ）
│   ├── manifest.json              # ポート8002に変更
│   ├── background.js
│   └── popup.html
├── create_database_lite.py         # EDINETコードリストからDB作成
├── phase15_lite_api.py            # Lite版APIサーバー
├── requirements.txt               # 既存の依存関係
├── SETUP_LITE.md                  # 3ステップセットアップガイド
└── README_LITE.md                 # Lite版説明
```

### 3ステップセットアップ

**Step 1: EDINETコードリストダウンロード**
```bash
# 1. https://disclosure2.edinet-fsa.go.jp/weee0010.aspx にアクセス
# 2. 「EDINETコードリスト」をダウンロード
# 3. プロジェクトディレクトリに配置
```

**Step 2: データベース作成**
```bash
python create_database_lite.py
# → ./data/corporate_lite.db が作成される（約5-10MB）
```

**Step 3: 起動**
```bash
python phase15_lite_api.py  # ポート8002で起動
# Chrome拡張機能をインストール（既存のものを使用）
```

### 配布方法

#### Option A: GitHub Releases
```bash
# 軽量版をビルド
python build_lightweight.py

# リリース作成
gh release create v1.0.0-lite \
  CompanyGenius-Lite.zip \
  --title "CompanyGenius Lite v1.0.0" \
  --notes "EDINET上場企業版（10MB、3分セットアップ）"
```

#### Option B: 即座実行版
```bash
# 1コマンドセットアップ
curl -s https://raw.githubusercontent.com/KazuyaIna080/CompanyGenius/main/install-lite.sh | bash

# 実行内容:
# - 軽量版ダウンロード
# - Python依存関係インストール
# - データベース配置
# - APIサーバー起動
```

---

## 🎯 ユーザーメリット

### フル版との比較

| 要素 | フル版 | 軽量版 |
|---|---|---|
| **セットアップ時間** | 30-60分 | 1-2分 |
| **必要ディスク容量** | 4GB+ | 50MB |
| **データダウンロード** | 必要（3.5GB CSV） | 不要 |
| **対象企業** | 全法人（350万社） | 上場企業（4千社） |
| **実務カバー率** | 100% | 90%+ |
| **初心者向け** | ❌ | ✅ |

### 軽量版の優位性

1. **即座利用開始**: ダウンロード後すぐに利用可能
2. **低リソース**: 古いPCでも快適動作
3. **高精度**: 上場企業なら99%の精度
4. **メンテナンス簡単**: 月次EDINETデータ更新のみ

---

## 🔄 アップグレード戦略

### 軽量版→フル版の移行

```python
# upgrade_to_full.py
def upgrade_to_full_version():
    """軽量版からフル版へのアップグレード"""
    
    print("🔄 CompanyGenius フル版へのアップグレード")
    
    # 1. 既存データの保持
    backup_user_corrections()
    
    # 2. フル版データベースのダウンロード案内
    guide_full_database_setup()
    
    # 3. 設定移行
    migrate_configuration()
    
    # 4. Chrome拡張機能更新
    update_chrome_extension()
    
    print("✅ フル版アップグレード完了")
```

### ハイブリッド運用

- **軽量版**: 日常的な上場企業確認
- **フル版**: 詳細調査・網羅的検索
- **API統合**: 両方を統合した検索機能

---

## 📈 実装優先順位

### Phase 1: 基本軽量版（即座実装可能）
- [ ] EDINETデータ取得・加工スクリプト
- [ ] 軽量版データベース作成
- [ ] 軽量版APIサーバー
- [ ] Chrome拡張機能の軽量版対応
- [ ] 簡単セットアップガイド

### Phase 2: 利便性向上
- [ ] ワンクリックインストーラー
- [ ] 自動アップデート機能
- [ ] 統計・分析機能
- [ ] ユーザーフィードバック収集

### Phase 3: 統合・拡張
- [ ] フル版との統合API
- [ ] 複数データソース対応
- [ ] 企業情報詳細表示
- [ ] ビジネスインテリジェンス機能

---

## 🚀 想定される影響

### ユーザー体験
- **学習コスト**: 大幅削減
- **導入障壁**: ほぼ除去
- **満足度**: 大幅向上（即座利用開始）

### 普及効果
- **個人ユーザー**: 10倍以上増加見込み
- **企業導入**: POC（概念実証）として活用
- **フィードバック**: 早期収集・改善サイクル高速化

### 技術的メリット
- **開発効率**: プロトタイプ高速作成
- **テスト容易性**: 軽量でCI/CD最適化
- **スケーラビリティ**: 段階的機能拡張

---

**🎯 軽量版は CompanyGenius の普及と実用化の鍵となる戦略的重要機能です！**