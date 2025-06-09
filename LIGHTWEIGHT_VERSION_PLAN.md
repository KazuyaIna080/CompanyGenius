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

```python
# lightweight_edinet_builder.py
import requests
import json
import sqlite3
from datetime import datetime

class EDINETLightweightBuilder:
    """EDINET軽量版データベース作成"""
    
    def __init__(self):
        self.api_key = "YOUR_EDINET_API_KEY"  # 要取得
        self.db_path = "./data/corporate_lightweight.db"
        self.companies = []
    
    def fetch_listed_companies(self):
        """EDINET APIから上場企業リストを取得"""
        url = "https://disclosure2dl.edinet-fsa.go.jp/api/v2/documents.json"
        
        # 過去1年の有価証券報告書を取得
        params = {
            'date': '2025-01-01',
            'type': '2',  # 有価証券報告書
            'Subscription-Key': self.api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        # 企業情報を抽出・正規化
        for doc in data.get('results', []):
            company_info = {
                'edinet_code': doc.get('edinetCode'),
                'company_name': doc.get('filerName'),
                'company_name_en': doc.get('filerNameEn'),
                'securities_code': doc.get('secCode'),
                'jcn': doc.get('JCN'),  # 法人番号
                'submit_date': doc.get('submitDateTime'),
                'business_category': self._extract_business_category(doc),
                'market_section': self._extract_market_section(doc)
            }
            self.companies.append(company_info)
    
    def create_lightweight_database(self):
        """軽量版データベース作成"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 軽量版テーブル作成
        cursor.execute('''
            CREATE TABLE companies_lite (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                edinet_code TEXT UNIQUE,
                company_name TEXT,
                company_name_en TEXT,
                securities_code TEXT,
                jcn TEXT,
                business_category TEXT,
                market_section TEXT,
                last_updated TEXT
            )
        ''')
        
        # データ挿入
        for company in self.companies:
            cursor.execute('''
                INSERT OR REPLACE INTO companies_lite 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                None, company['edinet_code'], company['company_name'],
                company['company_name_en'], company['securities_code'],
                company['jcn'], company['business_category'],
                company['market_section'], datetime.now().isoformat()
            ))
        
        # 検索用インデックス
        cursor.execute('CREATE INDEX idx_lite_name ON companies_lite(company_name)')
        cursor.execute('CREATE INDEX idx_lite_code ON companies_lite(securities_code)')
        
        conn.commit()
        conn.close()
        
        print(f"✅ 軽量版DB作成完了: {len(self.companies)} 社")
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

class LightweightPredictor:
    """軽量版予測システム"""
    
    def __init__(self):
        self.db_path = "./data/corporate_lightweight.db"
    
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

### 軽量版パッケージ構成

```
CompanyGenius-Lite/
├── data/
│   └── corporate_lightweight.db     # 10-20MB（事前構築済み）
├── chrome_extension_lite/          # 軽量版専用拡張機能
│   ├── manifest.json              # ポート8002に変更
│   ├── background.js
│   └── popup.html
├── phase15_lightweight_api.py      # 軽量版APIサーバー
├── requirements_lite.txt           # 最小依存関係
├── QUICK_START_LITE.md            # 3分セットアップガイド
└── README_LITE.md                 # 軽量版説明
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