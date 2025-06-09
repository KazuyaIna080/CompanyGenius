# 🏢 CompanyGenius Standard Edition 拡張機能設計

## 🎯 標準版の戦略的ポジショニング

**軽量版**: データベース内蔵、基本的な企業名予測
**標準版**: 予測 + 包括的企業情報検索・調査支援

---

## 🔍 外部検索機能の設計

### 企業名予測 → 多角的情報収集

```
企業名予測結果
    ↓
🌐 外部サイト検索ボタン群
├── 📖 Wikipedia
├── 💰 Yahoo!ファイナンス  
├── 📜 特許庁 商号検索
├── 🏛️ 法人番号公表サイト
├── 📊 EDINET検索
├── 🔍 Google検索
└── 📰 ニュース検索
```

### 実装アーキテクチャ

```javascript
class StandardEnhancedPredictor {
    constructor() {
        this.externalSearchProviders = {
            wikipedia: new WikipediaSearchProvider(),
            yahooFinance: new YahooFinanceSearchProvider(),
            jpo: new JPOSearchProvider(),
            houjinBangou: new HoujinBangouSearchProvider(),
            edinet: new EDINETSearchProvider(),
            google: new GoogleSearchProvider(),
            news: new NewsSearchProvider()
        };
    }
    
    async generateSearchLinks(companyName, securitiesCode, corporateNumber) {
        const links = {};
        
        for (const [provider, instance] of Object.entries(this.externalSearchProviders)) {
            links[provider] = await instance.generateSearchURL(
                companyName, 
                securitiesCode, 
                corporateNumber
            );
        }
        
        return links;
    }
}
```

---

## 📖 検索プロバイダー詳細設計

### 1. Wikipedia検索

```javascript
class WikipediaSearchProvider {
    generateSearchURL(companyName) {
        // 企業名の正規化
        const normalizedName = this.normalizeCompanyName(companyName);
        
        return {
            url: `https://ja.wikipedia.org/wiki/${encodeURIComponent(normalizedName)}`,
            fallbackUrl: `https://ja.wikipedia.org/w/index.php?search=${encodeURIComponent(normalizedName)}`,
            icon: '📖',
            label: 'Wikipedia',
            description: '企業概要・歴史・事業内容'
        };
    }
    
    normalizeCompanyName(name) {
        // "株式会社"などを除去して検索精度向上
        return name
            .replace(/株式会社/g, '')
            .replace(/\(株\)/g, '')
            .replace(/有限会社/g, '')
            .replace(/合同会社/g, '')
            .trim();
    }
}
```

### 2. Yahoo!ファイナンス検索

```javascript
class YahooFinanceSearchProvider {
    generateSearchURL(companyName, securitiesCode) {
        if (securitiesCode) {
            // 証券コードがある場合は直接リンク
            return {
                url: `https://finance.yahoo.co.jp/quote/${securitiesCode}.T`,
                icon: '💰',
                label: 'Yahoo!ファイナンス',
                description: '株価・財務情報・投資情報'
            };
        } else {
            // 企業名検索
            return {
                url: `https://finance.yahoo.co.jp/search?query=${encodeURIComponent(companyName)}`,
                icon: '💰',
                label: 'Yahoo!ファイナンス',
                description: '株価・財務情報検索'
            };
        }
    }
}
```

### 3. 特許庁 商号検索

```javascript
class JPOSearchProvider {
    generateSearchURL(companyName) {
        const normalizedName = companyName.replace(/株式会社|有限会社|合同会社/g, '').trim();
        
        return {
            url: `https://www.j-platpat.inpit.go.jp/c1800/PU/JP-2010-000001/15/ja`,
            searchUrl: `https://www.j-platpat.inpit.go.jp/web/all/top/BTmTopPage`,
            searchQuery: normalizedName,
            icon: '📜',
            label: '特許庁 J-PlatPat',
            description: '商標・特許・意匠・実用新案',
            note: '手動検索が必要'
        };
    }
}
```

### 4. 法人番号公表サイト検索

```javascript
class HoujinBangouSearchProvider {
    generateSearchURL(companyName, securitiesCode, corporateNumber) {
        if (corporateNumber) {
            // 法人番号が分かっている場合
            return {
                url: `https://www.houjin-bangou.nta.go.jp/henkorireki-johoto.html?selHouzinNo=${corporateNumber}`,
                icon: '🏛️',
                label: '法人番号公表サイト',
                description: '正式登記情報・変更履歴'
            };
        } else {
            // 企業名検索
            return {
                url: `https://www.houjin-bangou.nta.go.jp/kojinbango/kojinbango.html`,
                searchQuery: companyName,
                icon: '🏛️',
                label: '法人番号公表サイト',
                description: '法人番号・正式名称検索',
                note: '手動検索が必要'
            };
        }
    }
}
```

### 5. EDINET検索

```javascript
class EDINETSearchProvider {
    generateSearchURL(companyName, securitiesCode) {
        return {
            url: `https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx`,
            searchQuery: companyName,
            icon: '📊',
            label: 'EDINET',
            description: '有価証券報告書・決算短信',
            note: '手動検索が必要'
        };
    }
}
```

### 6. Google検索（企業情報特化）

```javascript
class GoogleSearchProvider {
    generateSearchURL(companyName) {
        const searchQuery = `"${companyName}" 企業情報 IR 会社概要`;
        
        return {
            url: `https://www.google.com/search?q=${encodeURIComponent(searchQuery)}`,
            icon: '🔍',
            label: 'Google企業検索',
            description: '公式サイト・IR情報・ニュース'
        };
    }
}
```

### 7. ニュース検索

```javascript
class NewsSearchProvider {
    generateSearchURL(companyName) {
        return {
            googleNews: `https://news.google.com/search?q=${encodeURIComponent(companyName)}&hl=ja&gl=JP&ceid=JP:ja`,
            yahooNews: `https://news.yahoo.co.jp/search?p=${encodeURIComponent(companyName)}`,
            icon: '📰',
            label: 'ニュース検索',
            description: '最新ニュース・プレスリリース'
        };
    }
}
```

---

## 🎨 UI/UX設計

### 予測結果 + 検索ボタン群

```html
<div class="prediction-result-enhanced">
    <!-- 基本予測結果 -->
    <div class="company-prediction">
        <h3>🏢 トヨタ自動車株式会社</h3>
        <div class="prediction-details">
            <span class="confidence">信頼度: 100%</span>
            <span class="securities-code">証券コード: 7203</span>
            <span class="source">ソース: EDINET完全一致</span>
        </div>
    </div>
    
    <!-- 外部検索ボタン群 -->
    <div class="external-search-panel">
        <h4>🔍 関連情報を検索</h4>
        
        <div class="search-buttons-grid">
            <button class="search-btn wikipedia" data-provider="wikipedia">
                📖 Wikipedia
                <span class="btn-desc">企業概要・歴史</span>
            </button>
            
            <button class="search-btn finance" data-provider="yahooFinance">
                💰 Yahoo!ファイナンス
                <span class="btn-desc">株価・財務情報</span>
            </button>
            
            <button class="search-btn jpo" data-provider="jpo">
                📜 特許庁検索
                <span class="btn-desc">商標・特許情報</span>
            </button>
            
            <button class="search-btn houjin" data-provider="houjinBangou">
                🏛️ 法人番号検索
                <span class="btn-desc">正式登記情報</span>
            </button>
            
            <button class="search-btn edinet" data-provider="edinet">
                📊 EDINET
                <span class="btn-desc">有価証券報告書</span>
            </button>
            
            <button class="search-btn google" data-provider="google">
                🔍 Google検索
                <span class="btn-desc">公式サイト・IR</span>
            </button>
        </div>
        
        <!-- ニュース検索（特別扱い） -->
        <div class="news-search-section">
            <h5>📰 最新ニュース</h5>
            <div class="news-buttons">
                <button class="search-btn news-google" data-provider="googleNews">
                    Google ニュース
                </button>
                <button class="search-btn news-yahoo" data-provider="yahooNews">
                    Yahoo! ニュース
                </button>
            </div>
        </div>
    </div>
    
    <!-- ワンクリック全検索 -->
    <div class="batch-search-section">
        <button class="batch-search-btn">
            🚀 すべてのサイトで検索（新しいタブで一括オープン）
        </button>
    </div>
</div>
```

### CSS スタイリング

```css
.external-search-panel {
    margin-top: 16px;
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
    border: 1px solid #e9ecef;
}

.search-buttons-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 8px;
    margin-bottom: 16px;
}

.search-btn {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 12px;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    background: white;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
    font-size: 14px;
    font-weight: 600;
}

.search-btn:hover {
    background: #e9ecef;
    border-color: #adb5bd;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.search-btn .btn-desc {
    font-size: 11px;
    font-weight: 400;
    color: #6c757d;
    margin-top: 2px;
}

.batch-search-btn {
    width: 100%;
    padding: 14px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.batch-search-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
```

---

## 🔧 実装フロー

### Phase 1: 基本外部検索機能
- [ ] 検索プロバイダークラス実装
- [ ] UI/UX コンポーネント作成
- [ ] 各サイトのURL生成ロジック
- [ ] 新しいタブでのリンク開機能

### Phase 2: 高度な検索機能
- [ ] 証券コード・法人番号による最適化検索
- [ ] 一括検索機能（複数タブ同時オープン）
- [ ] 検索履歴・ブックマーク機能
- [ ] カスタム検索プロバイダー追加機能

### Phase 3: インテリジェント検索
- [ ] 企業属性（上場/非上場、業種等）による検索最適化
- [ ] 検索結果のプレビュー機能
- [ ] AIによる関連企業・競合企業提案
- [ ] 業界分析・比較機能

---

## 📊 期待される効果

### ユーザー価値向上
- **時間短縮**: 企業調査時間を70%削減
- **情報包括性**: 複数ソースからの一括情報収集
- **正確性**: 公式情報源への直接アクセス

### 差別化要因
- **軽量版**: 基本的な企業名予測
- **標準版**: 予測 + 包括的企業調査支援
- **付加価値**: 単純検索ツールから調査プラットフォームへ

### 利用場面
- **営業**: 顧客企業の事前調査
- **投資**: 投資対象企業の多角的分析  
- **研究**: 学術・市場調査
- **法務**: 企業の正式情報確認

---

**🎯 標準版は「企業名予測」から「企業調査プラットフォーム」への進化を実現します！**