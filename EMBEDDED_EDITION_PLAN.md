# 🔗 CompanyGenius Embedded Edition - 革命的ゼロ設定版

## 🎯 コンセプト

**Chrome Web Storeからワンクリックインストール→即座利用開始**

EDINETデータベースを内蔵したChrome拡張機能で、セットアップ・APIサーバー・ネットワーク接続が一切不要の革新的アプローチ。

---

## 📊 容量制限の確認

### Chrome拡張機能の制限
| 配布方法 | 容量制限 | EDINETデータベース |
|---|---|---|
| **Chrome Web Store** | 128MB | ✅ 5-10MB（十分余裕） |
| **開発者モード** | 制限なし | ✅ 問題なし |

### 内蔵データ構成
- **EDINETデータベース**: 5-10MB（SQLite形式）
- **sql.js ライブラリ**: 1-2MB（WebAssembly SQLite）
- **拡張機能コード**: 1MB未満
- **合計**: 10-15MB（128MB制限の10%程度）

---

## 🏗️ 技術アーキテクチャ

### 拡張機能構成
```
CompanyGenius-Embedded/
├── manifest.json              # Manifest V3設定
├── background.js               # Service Worker + SQLite制御
├── popup.html/js               # ポップアップUI
├── content.js                  # 右クリックメニュー・DOM操作
├── data/
│   └── corporate_embedded.db   # 内蔵EDINETデータベース（5-10MB）
├── lib/
│   ├── sql-wasm.js            # sql.js WebAssembly SQLite
│   └── sql-wasm.wasm          # SQLite WebAssembly バイナリ
├── icons/                      # 拡張機能アイコン
└── styles/                     # CSS
```

### 技術スタック
- **Manifest V3**: 最新Chrome拡張機能仕様
- **sql.js**: WebAssemblyベースSQLite（ブラウザ内実行）
- **Service Worker**: バックグラウンド処理
- **IndexedDB**: ユーザー学習データ永続化

---

## 🔧 実装詳細

### SQLite in Browser（sql.js）

```javascript
// background.js - Service Worker
import initSqlJs from './lib/sql-wasm.js';

class EmbeddedCompanyDatabase {
    constructor() {
        this.db = null;
        this.userCorrections = new Map();
    }
    
    async initialize() {
        // sql.js初期化
        const SQL = await initSqlJs({
            locateFile: file => `./lib/${file}`
        });
        
        // 内蔵データベースファイル読み込み
        const dbFile = await fetch('./data/corporate_embedded.db');
        const dbBuffer = await dbFile.arrayBuffer();
        
        // SQLiteデータベースをメモリに展開
        this.db = new SQL.Database(new Uint8Array(dbBuffer));
        
        console.log('🔗 CompanyGenius Embedded Database initialized');
        
        // ユーザー学習データ読み込み
        await this.loadUserCorrections();
    }
    
    async predict(query) {
        // Level 1: ユーザー学習データ（最優先）
        if (this.userCorrections.has(query)) {
            return {
                prediction: this.userCorrections.get(query).correct_name,
                confidence: 1.0,
                source: 'user_learning'
            };
        }
        
        // Level 2: EDINET完全一致
        const exactMatch = this.db.exec(`
            SELECT company_name, securities_code 
            FROM companies_lite 
            WHERE company_name = ?
        `, [query]);
        
        if (exactMatch.length > 0) {
            return {
                prediction: exactMatch[0].values[0][0],
                securities_code: exactMatch[0].values[0][1],
                confidence: 1.0,
                source: 'edinet_exact'
            };
        }
        
        // Level 3: 部分一致・推定
        const partialMatch = this.db.exec(`
            SELECT company_name, securities_code 
            FROM companies_lite 
            WHERE company_name LIKE ? 
            LIMIT 3
        `, [`%${query}%`]);
        
        if (partialMatch.length > 0) {
            return {
                prediction: partialMatch[0].values[0][0],
                securities_code: partialMatch[0].values[0][1],
                confidence: 0.8,
                source: 'edinet_partial',
                alternatives: partialMatch[0].values.slice(1).map(row => ({
                    name: row[0],
                    code: row[1]
                }))
            };
        }
        
        // Level 4: 基本推定
        return {
            prediction: `${query}株式会社`,
            confidence: 0.3,
            source: 'estimation'
        };
    }
    
    async addUserCorrection(originalQuery, predictedName, correctName) {
        // ユーザー学習データ追加
        this.userCorrections.set(originalQuery, {
            predicted_name: predictedName,
            correct_name: correctName,
            timestamp: new Date().toISOString()
        });
        
        // IndexedDBに永続化
        await this.saveUserCorrections();
        
        console.log(`📚 User correction added: ${originalQuery} → ${correctName}`);
    }
    
    async loadUserCorrections() {
        // IndexedDBからユーザー学習データ読み込み
        // 実装省略
    }
    
    async saveUserCorrections() {
        // IndexedDBにユーザー学習データ保存
        // 実装省略
    }
}

// グローバルインスタンス
const companyDB = new EmbeddedCompanyDatabase();

// 拡張機能起動時に初期化
chrome.runtime.onStartup.addListener(async () => {
    await companyDB.initialize();
});

chrome.runtime.onInstalled.addListener(async () => {
    await companyDB.initialize();
});

// メッセージハンドラ
chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
    if (request.action === 'predict') {
        const result = await companyDB.predict(request.query);
        sendResponse(result);
    } else if (request.action === 'correct') {
        await companyDB.addUserCorrection(
            request.originalQuery,
            request.predictedName,
            request.correctName
        );
        sendResponse({ success: true });
    }
    return true; // 非同期レスポンス
});
```

### ポップアップUI更新

```javascript
// popup.js - ポップアップインターフェース
class EmbeddedPopup {
    constructor() {
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        document.getElementById('predictBtn').addEventListener('click', 
            () => this.predictCompany());
    }
    
    async predictCompany() {
        const query = document.getElementById('companyInput').value.trim();
        if (!query) return;
        
        // バックグラウンドスクリプトに予測リクエスト
        const result = await chrome.runtime.sendMessage({
            action: 'predict',
            query: query
        });
        
        this.displayResult(result);
    }
    
    displayResult(result) {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `
            <div class="prediction-result">
                <h3>🏢 予測結果</h3>
                <div class="company-name">${result.prediction}</div>
                <div class="confidence">信頼度: ${(result.confidence * 100).toFixed(0)}%</div>
                <div class="source">ソース: ${this.getSourceLabel(result.source)}</div>
                ${result.securities_code ? `<div class="securities-code">証券コード: ${result.securities_code}</div>` : ''}
                
                <div class="action-buttons">
                    <button id="correctBtn" class="correct-btn">❌ 間違い</button>
                    <button id="acceptBtn" class="accept-btn">✅ 正解</button>
                </div>
            </div>
        `;
        
        // 修正ボタンのイベントリスナー
        document.getElementById('correctBtn').addEventListener('click', 
            () => this.showCorrectionDialog(query, result.prediction));
    }
    
    getSourceLabel(source) {
        const labels = {
            'user_learning': '🧠 ユーザー学習',
            'edinet_exact': '🎯 EDINET完全一致',
            'edinet_partial': '🔍 EDINET部分一致',
            'estimation': '💭 推定'
        };
        return labels[source] || source;
    }
    
    async showCorrectionDialog(originalQuery, predictedName) {
        const correctName = prompt(`正しい企業名を入力してください:\n\n検索語: ${originalQuery}\n予測結果: ${predictedName}\n\n正解:`);
        
        if (correctName && correctName.trim()) {
            await chrome.runtime.sendMessage({
                action: 'correct',
                originalQuery: originalQuery,
                predictedName: predictedName,
                correctName: correctName.trim()
            });
            
            alert('✅ 学習データを更新しました');
        }
    }
}

// ポップアップ初期化
document.addEventListener('DOMContentLoaded', () => {
    new EmbeddedPopup();
});
```

---

## 📦 ビルド・配布プロセス

### データベース作成パイプライン

```python
# build_embedded_edition.py
import sqlite3
import os
import shutil
from pathlib import Path

def build_embedded_database():
    """内蔵用EDINETデータベース作成"""
    
    print("🔗 CompanyGenius Embedded Edition ビルド")
    
    # 1. EDINETコードリストからデータベース作成
    # （既存のcreate_database_lite.pyを活用）
    
    # 2. データベース最適化（容量削減）
    optimize_embedded_database()
    
    # 3. Chrome拡張機能ディレクトリにコピー
    copy_to_extension_dir()

def optimize_embedded_database():
    """内蔵用データベース最適化"""
    
    conn = sqlite3.connect('./data/corporate_lite.db')
    cursor = conn.cursor()
    
    # 不要なフィールド削除（容量削減）
    cursor.execute('''
        CREATE TABLE companies_optimized AS
        SELECT 
            edinet_code,
            company_name,
            company_name_kana,
            securities_code,
            corporate_number
        FROM companies_lite
        WHERE company_name IS NOT NULL 
        AND company_name != ''
    ''')
    
    # 元テーブル削除
    cursor.execute('DROP TABLE companies_lite')
    cursor.execute('ALTER TABLE companies_optimized RENAME TO companies_lite')
    
    # インデックス再構築
    cursor.execute('CREATE INDEX idx_name ON companies_lite(company_name)')
    cursor.execute('CREATE INDEX idx_kana ON companies_lite(company_name_kana)')
    
    # VACUUM（容量最適化）
    cursor.execute('VACUUM')
    
    conn.close()
    
    # ファイルサイズ確認
    size = os.path.getsize('./data/corporate_lite.db') / (1024 * 1024)
    print(f"📊 最適化後データベースサイズ: {size:.1f} MB")

def copy_to_extension_dir():
    """Chrome拡張機能ディレクトリにコピー"""
    
    extension_dir = './chrome_extension_embedded'
    os.makedirs(f"{extension_dir}/data", exist_ok=True)
    
    # データベースファイルコピー
    shutil.copy2(
        './data/corporate_lite.db',
        f'{extension_dir}/data/corporate_embedded.db'
    )
    
    print(f"✅ Embedded Edition ビルド完了: {extension_dir}")

if __name__ == "__main__":
    build_embedded_database()
```

### Chrome Web Store配布

```json
// manifest.json
{
  "manifest_version": 3,
  "name": "CompanyGenius Embedded",
  "version": "1.0.0",
  "description": "企業名予測・正式社名確認（データベース内蔵版）- セットアップ不要",
  
  "permissions": [
    "storage",
    "activeTab",
    "contextMenus"
  ],
  
  "background": {
    "service_worker": "background.js",
    "type": "module"
  },
  
  "action": {
    "default_popup": "popup.html"
  },
  
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "run_at": "document_end"
    }
  ],
  
  "web_accessible_resources": [
    {
      "resources": ["lib/*.wasm"],
      "matches": ["<all_urls>"]
    }
  ]
}
```

---

## 🚀 ユーザー体験の革命

### 従来版 vs Embedded Edition

| 要素 | Lite Edition | **Embedded Edition** |
|---|---|---|
| **インストール** | Chrome拡張機能 + セットアップ | Chrome Web Store ワンクリック |
| **セットアップ時間** | 1-2分 | **0秒** |
| **必要な作業** | CSVダウンロード + DB作成 | **なし** |
| **APIサーバー** | 必要（localhost:8002） | **不要** |
| **ネットワーク** | 必要 | **不要（オフライン動作）** |
| **セキュリティ** | ローカルサーバー | **完全ローカル処理** |
| **レスポンス** | HTTP通信 | **瞬間（メモリ内）** |

### ユーザージャーニー
1. **Chrome Web Store で検索**: "CompanyGenius"
2. **ワンクリックインストール**: "Chromeに追加"
3. **即座利用開始**: セットアップ・設定一切不要
4. **学習機能**: ユーザー修正が自動で学習・改善

---

## 📈 市場インパクト

### 普及効果の予測
- **個人ユーザー**: 100倍以上の導入障壁削減
- **企業ユーザー**: IT管理者承認不要の簡単導入
- **教育機関**: 学生・研究者の気軽な利用
- **国際ユーザー**: 日本企業研究での活用

### 競合優位性
- **世界初**: 企業名予測機能のデータベース内蔵Chrome拡張機能
- **技術革新**: WebAssembly SQLiteの実用活用
- **ユーザビリティ**: ゼロ設定の究極体験

---

## 🔄 バージョン戦略改訂

### 新しい推奨順序

1. **🔗 Embedded Edition** (最推奨)
   - Chrome Web Store配布
   - データベース内蔵（5-10MB）
   - ゼロ設定・ワンクリックインストール

2. **🪶 Lite Edition** (中級者向け)
   - GitHub配布
   - ローカルセットアップ版
   - カスタマイズ可能

3. **🏢 Full Edition** (上級者・本格運用)
   - GitHub配布
   - 350万社完全データベース
   - 企業・研究用途

### 移行パス
- **Embedded → Full**: データ容量が必要な場合
- **どのバージョンでも**: ユーザー学習データ互換

---

**🎯 Embedded Editionにより、CompanyGeniusが世界で最も使いやすい企業名予測ツールになります！**

Chrome Web Store公開で、全世界のChromeユーザーが即座にアクセス可能になる革命的アプローチです。