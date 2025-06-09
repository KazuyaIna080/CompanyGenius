// CompanyGenius Embedded - Popup Script
// ポップアップUIの制御

class EmbeddedPopup {
    constructor() {
        this.currentResult = null;
        this.currentQuery = '';
        this.init();
    }
    
    async init() {
        this.setupEventListeners();
        await this.loadStats();
        
        // 入力フィールドにフォーカス
        document.getElementById('companyInput').focus();
    }
    
    setupEventListeners() {
        // 予測ボタン
        document.getElementById('predictBtn').addEventListener('click', () => {
            this.predictCompany();
        });
        
        // Enter キーで予測実行
        document.getElementById('companyInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.predictCompany();
            }
        });
        
        // リアルタイム入力検証
        document.getElementById('companyInput').addEventListener('input', (e) => {
            const btn = document.getElementById('predictBtn');
            btn.disabled = !e.target.value.trim();
        });
        
        // アクションボタン
        document.getElementById('correctBtn').addEventListener('click', () => {
            this.showCorrectionDialog();
        });
        
        document.getElementById('acceptBtn').addEventListener('click', () => {
            this.acceptPrediction();
        });
    }
    
    async predictCompany() {
        const query = document.getElementById('companyInput').value.trim();
        if (!query) return;
        
        this.currentQuery = query;
        this.showLoading(true);
        this.hideError();
        this.hideResult();
        
        try {
            // バックグラウンドスクリプトに予測リクエスト
            const result = await this.sendMessage({ action: 'predict', query });
            
            this.currentResult = result;
            this.displayResult(result);
            
        } catch (error) {
            console.error('Prediction error:', error);
            this.showError('予測中にエラーが発生しました: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }
    
    displayResult(result) {
        const resultSection = document.getElementById('resultSection');
        const companyName = document.getElementById('companyName');
        const resultDetails = document.getElementById('resultDetails');
        const resultIcon = document.getElementById('resultIcon');
        
        // 企業名表示
        companyName.textContent = result.prediction;
        
        // 詳細情報
        let details = [];
        details.push(`信頼度: ${(result.confidence * 100).toFixed(0)}%`);
        details.push(`ソース: ${this.getSourceLabel(result.source)}`);
        
        if (result.securities_code) {
            details.push(`証券コード: ${result.securities_code}`);
        }
        
        if (result.timestamp) {
            const date = new Date(result.timestamp).toLocaleDateString('ja-JP');
            details.push(`学習日: ${date}`);
        }
        
        if (result.note) {
            details.push(`📝 ${result.note}`);
        }
        
        resultDetails.innerHTML = details.map(detail => `<div>${detail}</div>`).join('');
        
        // アイコン設定
        resultIcon.textContent = this.getSourceIcon(result.source);
        
        // 結果セクション表示
        resultSection.style.display = 'block';
        
        // 代替候補があれば表示
        if (result.alternatives && result.alternatives.length > 0) {
            this.displayAlternatives(result.alternatives);
        }
    }
    
    displayAlternatives(alternatives) {
        const resultDetails = document.getElementById('resultDetails');
        const currentContent = resultDetails.innerHTML;
        
        const alternativesHtml = alternatives.map(alt => 
            `<div style="margin-left: 12px; font-size: 11px; opacity: 0.8;">
                📋 ${alt.name} ${alt.code ? `(${alt.code})` : ''}
            </div>`
        ).join('');
        
        resultDetails.innerHTML = currentContent + 
            '<div style="margin-top: 8px; font-size: 11px;">その他の候補:</div>' + 
            alternativesHtml;
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
    
    getSourceIcon(source) {
        const icons = {
            'user_learning': '🧠',
            'edinet_exact': '🎯',
            'edinet_partial': '🔍',
            'estimation': '💭'
        };
        return icons[source] || '🏢';
    }
    
    async showCorrectionDialog() {
        if (!this.currentResult || !this.currentQuery) return;
        
        const correctName = prompt(
            `正しい企業名を入力してください:\n\n` +
            `検索語: ${this.currentQuery}\n` +
            `予測結果: ${this.currentResult.prediction}\n\n` +
            `正解:`
        );
        
        if (correctName && correctName.trim() && correctName.trim() !== this.currentResult.prediction) {
            try {
                await this.sendMessage({
                    action: 'correct',
                    originalQuery: this.currentQuery,
                    predictedName: this.currentResult.prediction,
                    correctName: correctName.trim()
                });
                
                alert('✅ 学習データを更新しました！次回からより正確な予測を行います。');
                
                // 統計更新
                await this.loadStats();
                
            } catch (error) {
                console.error('Correction error:', error);
                this.showError('学習データの更新に失敗しました: ' + error.message);
            }
        }
    }
    
    acceptPrediction() {
        alert('✅ フィードバックありがとうございます！');
        this.hideResult();
        document.getElementById('companyInput').value = '';
        document.getElementById('companyInput').focus();
    }
    
    async loadStats() {
        try {
            const stats = await this.sendMessage({ action: 'getStats' });
            
            document.getElementById('totalCompanies').textContent = 
                stats.total_companies ? `${stats.total_companies.toLocaleString()}社` : '-';
            document.getElementById('userCorrections').textContent = 
                stats.user_corrections ? `${stats.user_corrections}件` : '0件';
            document.getElementById('databaseType').textContent = 
                stats.database_type === 'embedded' ? '内蔵版' : stats.database_type || '-';
                
        } catch (error) {
            console.error('Stats loading error:', error);
        }
    }
    
    showLoading(show) {
        const loadingSection = document.getElementById('loadingSection');
        loadingSection.style.display = show ? 'block' : 'none';
        
        const predictBtn = document.getElementById('predictBtn');
        predictBtn.disabled = show;
    }
    
    showError(message) {
        const errorSection = document.getElementById('errorSection');
        errorSection.textContent = message;
        errorSection.style.display = 'block';
        
        setTimeout(() => {
            this.hideError();
        }, 5000);
    }
    
    hideError() {
        document.getElementById('errorSection').style.display = 'none';
    }
    
    hideResult() {
        document.getElementById('resultSection').style.display = 'none';
    }
    
    // Chrome拡張機能メッセージング
    sendMessage(message) {
        return new Promise((resolve, reject) => {
            chrome.runtime.sendMessage(message, (response) => {
                if (chrome.runtime.lastError) {
                    reject(new Error(chrome.runtime.lastError.message));
                } else if (response && response.error) {
                    reject(new Error(response.error));
                } else {
                    resolve(response);
                }
            });
        });
    }
}

// ポップアップ初期化
document.addEventListener('DOMContentLoaded', () => {
    new EmbeddedPopup();
});

console.log('🔗 CompanyGenius Embedded popup loaded');