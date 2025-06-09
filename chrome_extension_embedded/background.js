// CompanyGenius Embedded - Background Script (Service Worker)
// データベース内蔵型企業名予測システム

class EmbeddedCompanyDatabase {
    constructor() {
        this.db = null;
        this.SQL = null;
        this.userCorrections = new Map();
        this.isInitialized = false;
    }
    
    async initialize() {
        if (this.isInitialized) return;
        
        console.log('🔗 CompanyGenius Embedded Database initializing...');
        
        try {
            // sql.js動的インポート（Chrome拡張機能では静的インポートを使用）
            // 実際の実装ではsql.jsライブラリを組み込む必要がある
            
            // 暫定的にダミーデータベースで動作確認
            this.initializeDummyDatabase();
            
            // ユーザー学習データ読み込み
            await this.loadUserCorrections();
            
            this.isInitialized = true;
            console.log('✅ CompanyGenius Embedded Database initialized');
            
        } catch (error) {
            console.error('❌ Database initialization failed:', error);
        }
    }
    
    initializeDummyDatabase() {
        // 開発用ダミーデータ（実際の実装ではEDINETデータベースを使用）
        this.dummyCompanies = new Map([
            ['トヨタ', { name: 'トヨタ自動車株式会社', code: '7203', confidence: 1.0 }],
            ['ソニー', { name: 'ソニーグループ株式会社', code: '6758', confidence: 1.0 }],
            ['ソフトバンク', { name: 'ソフトバンクグループ株式会社', code: '9984', confidence: 1.0 }],
            ['任天堂', { name: '任天堂株式会社', code: '7974', confidence: 1.0 }],
            ['キーエンス', { name: '株式会社キーエンス', code: '6861', confidence: 1.0 }],
            ['ファナック', { name: 'ファナック株式会社', code: '6954', confidence: 1.0 }],
            ['信越化学', { name: '信越化学工業株式会社', code: '4063', confidence: 1.0 }],
            ['東京エレクトロン', { name: '株式会社東京エレクトロン', code: '8035', confidence: 1.0 }],
            ['ダイキン', { name: 'ダイキン工業株式会社', code: '6367', confidence: 1.0 }],
            ['KDDI', { name: 'KDDI株式会社', code: '9433', confidence: 1.0 }]
        ]);
        
        console.log('📊 Dummy database loaded:', this.dummyCompanies.size, 'companies');
    }
    
    async predict(query) {
        if (!this.isInitialized) {
            await this.initialize();
        }
        
        const normalizedQuery = query.trim();
        
        // Level 1: ユーザー学習データ（最優先）
        if (this.userCorrections.has(normalizedQuery)) {
            const correction = this.userCorrections.get(normalizedQuery);
            return {
                prediction: correction.correct_name,
                confidence: 1.0,
                source: 'user_learning',
                timestamp: correction.timestamp
            };
        }
        
        // Level 2: 完全一致検索
        if (this.dummyCompanies.has(normalizedQuery)) {
            const company = this.dummyCompanies.get(normalizedQuery);
            return {
                prediction: company.name,
                securities_code: company.code,
                confidence: company.confidence,
                source: 'edinet_exact'
            };
        }
        
        // Level 3: 部分一致検索
        const partialMatches = [];
        for (const [key, company] of this.dummyCompanies) {
            if (key.includes(normalizedQuery) || company.name.includes(normalizedQuery)) {
                partialMatches.push({
                    name: company.name,
                    code: company.code,
                    score: this.calculateMatchScore(normalizedQuery, key, company.name)
                });
            }
        }
        
        if (partialMatches.length > 0) {
            partialMatches.sort((a, b) => b.score - a.score);
            return {
                prediction: partialMatches[0].name,
                securities_code: partialMatches[0].code,
                confidence: 0.8,
                source: 'edinet_partial',
                alternatives: partialMatches.slice(1, 3)
            };
        }
        
        // Level 4: 基本推定
        const estimatedName = this.generateEstimatedName(normalizedQuery);
        return {
            prediction: estimatedName,
            confidence: 0.3,
            source: 'estimation',
            note: '推定結果です。正確な情報は公式サイトでご確認ください。'
        };
    }
    
    calculateMatchScore(query, key, name) {
        let score = 0;
        
        // 完全一致ボーナス
        if (key === query || name === query) score += 100;
        
        // 前方一致ボーナス
        if (key.startsWith(query) || name.startsWith(query)) score += 50;
        
        // 含有ボーナス
        if (key.includes(query)) score += 30;
        if (name.includes(query)) score += 20;
        
        // 長さによる調整
        score += Math.max(0, 20 - Math.abs(key.length - query.length));
        
        return score;
    }
    
    generateEstimatedName(query) {
        // 基本的な推定ルール
        if (query.endsWith('株式会社') || query.endsWith('(株)')) {
            return query;
        } else if (query.startsWith('株式会社')) {
            return query;
        } else {
            // 一般的なパターンで推定
            return `${query}株式会社`;
        }
    }
    
    async addUserCorrection(originalQuery, predictedName, correctName) {
        const normalizedQuery = originalQuery.trim();
        
        const correction = {
            predicted_name: predictedName,
            correct_name: correctName,
            timestamp: new Date().toISOString()
        };
        
        this.userCorrections.set(normalizedQuery, correction);
        
        // Chrome storage に保存
        await this.saveUserCorrections();
        
        console.log('📚 User correction added:', normalizedQuery, '→', correctName);
        
        return { success: true };
    }
    
    async loadUserCorrections() {
        try {
            const result = await chrome.storage.local.get(['userCorrections']);
            if (result.userCorrections) {
                this.userCorrections = new Map(Object.entries(result.userCorrections));
                console.log('📖 User corrections loaded:', this.userCorrections.size, 'entries');
            }
        } catch (error) {
            console.error('❌ Failed to load user corrections:', error);
        }
    }
    
    async saveUserCorrections() {
        try {
            const correctionsObject = Object.fromEntries(this.userCorrections);
            await chrome.storage.local.set({ userCorrections: correctionsObject });
            console.log('💾 User corrections saved');
        } catch (error) {
            console.error('❌ Failed to save user corrections:', error);
        }
    }
    
    async getStats() {
        await this.initialize();
        
        return {
            total_companies: this.dummyCompanies.size,
            user_corrections: this.userCorrections.size,
            database_type: 'embedded',
            version: '1.0.0-embedded'
        };
    }
}

// グローバルインスタンス
const companyDB = new EmbeddedCompanyDatabase();

// 拡張機能インストール時の初期化
chrome.runtime.onInstalled.addListener(async (details) => {
    console.log('🚀 CompanyGenius Embedded installed:', details.reason);
    
    // コンテキストメニュー作成
    chrome.contextMenus.create({
        id: 'companygenius-predict',
        title: 'CompanyGeniusで企業名を予測',
        contexts: ['selection']
    });
    
    await companyDB.initialize();
});

// 拡張機能起動時の初期化
chrome.runtime.onStartup.addListener(async () => {
    console.log('🔄 CompanyGenius Embedded startup');
    await companyDB.initialize();
});

// コンテキストメニュークリックハンドラ
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
    if (info.menuItemId === 'companygenius-predict') {
        const selectedText = info.selectionText.trim();
        if (selectedText) {
            const result = await companyDB.predict(selectedText);
            
            // コンテンツスクリプトに結果を送信
            chrome.tabs.sendMessage(tab.id, {
                action: 'showPredictionDialog',
                query: selectedText,
                result: result
            });
        }
    }
});

// メッセージハンドラ
chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
    try {
        switch (request.action) {
            case 'predict':
                const result = await companyDB.predict(request.query);
                sendResponse(result);
                break;
                
            case 'correct':
                const correctionResult = await companyDB.addUserCorrection(
                    request.originalQuery,
                    request.predictedName,
                    request.correctName
                );
                sendResponse(correctionResult);
                break;
                
            case 'getStats':
                const stats = await companyDB.getStats();
                sendResponse(stats);
                break;
                
            default:
                sendResponse({ error: 'Unknown action' });
        }
    } catch (error) {
        console.error('❌ Message handler error:', error);
        sendResponse({ error: error.message });
    }
    
    return true; // 非同期レスポンスを示す
});

console.log('🔗 CompanyGenius Embedded background script loaded');