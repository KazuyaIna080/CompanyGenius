// CompanyGenius Embedded - Content Script
// 右クリックメニューとページ内インタラクション

class EmbeddedContent {
    constructor() {
        this.currentDialog = null;
        this.init();
    }
    
    init() {
        console.log('🔗 CompanyGenius Embedded content script loaded for:', window.location.hostname);
        
        // メッセージリスナー設定
        chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
            this.handleMessage(message, sender, sendResponse);
            return true; // 非同期レスポンス
        });
    }
    
    async handleMessage(message, sender, sendResponse) {
        try {
            switch (message.action) {
                case 'showPredictionDialog':
                    await this.showPredictionDialog(message.query, message.result);
                    sendResponse({ success: true });
                    break;
                    
                default:
                    sendResponse({ error: 'Unknown action' });
            }
        } catch (error) {
            console.error('Content script error:', error);
            sendResponse({ error: error.message });
        }
    }
    
    async showPredictionDialog(query, result) {
        // 既存のダイアログがあれば削除
        this.removePredictionDialog();
        
        // ダイアログ作成
        const dialog = this.createPredictionDialog(query, result);
        document.body.appendChild(dialog);
        
        this.currentDialog = dialog;
        
        // アニメーション
        requestAnimationFrame(() => {
            dialog.classList.add('show');
        });
        
        // 自動クローズタイマー（10秒）
        setTimeout(() => {
            this.removePredictionDialog();
        }, 10000);
    }
    
    createPredictionDialog(query, result) {
        const dialog = document.createElement('div');
        dialog.className = 'companygenius-dialog';
        dialog.innerHTML = `
            <div class="companygenius-dialog-content">
                <div class="companygenius-header">
                    <span class="companygenius-icon">${this.getSourceIcon(result.source)}</span>
                    <span class="companygenius-title">CompanyGenius</span>
                    <button class="companygenius-close">&times;</button>
                </div>
                
                <div class="companygenius-body">
                    <div class="companygenius-query">
                        <strong>検索:</strong> "${query}"
                    </div>
                    
                    <div class="companygenius-result">
                        <div class="companygenius-company-name">${result.prediction}</div>
                        <div class="companygenius-details">
                            <div>信頼度: ${(result.confidence * 100).toFixed(0)}%</div>
                            <div>ソース: ${this.getSourceLabel(result.source)}</div>
                            ${result.securities_code ? `<div>証券コード: ${result.securities_code}</div>` : ''}
                        </div>
                    </div>
                    
                    ${result.alternatives ? this.renderAlternatives(result.alternatives) : ''}
                    
                    <div class="companygenius-actions">
                        <button class="companygenius-btn companygenius-correct-btn" data-action="correct">
                            ❌ 間違い
                        </button>
                        <button class="companygenius-btn companygenius-accept-btn" data-action="accept">
                            ✅ 正解
                        </button>
                    </div>
                    
                    ${result.note ? `<div class="companygenius-note">📝 ${result.note}</div>` : ''}
                </div>
            </div>
        `;
        
        // スタイル追加
        this.addDialogStyles();
        
        // イベントリスナー
        this.setupDialogEventListeners(dialog, query, result);
        
        return dialog;
    }
    
    renderAlternatives(alternatives) {
        if (!alternatives || alternatives.length === 0) return '';
        
        const altHtml = alternatives.map(alt => 
            `<div class="companygenius-alternative">
                📋 ${alt.name} ${alt.code ? `(${alt.code})` : ''}
            </div>`
        ).join('');
        
        return `
            <div class="companygenius-alternatives">
                <div class="companygenius-alternatives-title">その他の候補:</div>
                ${altHtml}
            </div>
        `;
    }
    
    setupDialogEventListeners(dialog, query, result) {
        // 閉じるボタン
        dialog.querySelector('.companygenius-close').addEventListener('click', () => {
            this.removePredictionDialog();
        });
        
        // アクションボタン
        dialog.querySelectorAll('.companygenius-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const action = e.target.dataset.action;
                
                if (action === 'correct') {
                    await this.handleCorrection(query, result);
                } else if (action === 'accept') {
                    this.handleAccept();
                }
                
                this.removePredictionDialog();
            });
        });
        
        // 外側クリックで閉じる
        dialog.addEventListener('click', (e) => {
            if (e.target === dialog) {
                this.removePredictionDialog();
            }
        });
    }
    
    async handleCorrection(query, result) {
        const correctName = prompt(
            `正しい企業名を入力してください:\n\n` +
            `検索語: ${query}\n` +
            `予測結果: ${result.prediction}\n\n` +
            `正解:`
        );
        
        if (correctName && correctName.trim() && correctName.trim() !== result.prediction) {
            try {
                await this.sendMessage({
                    action: 'correct',
                    originalQuery: query,
                    predictedName: result.prediction,
                    correctName: correctName.trim()
                });
                
                this.showNotification('✅ 学習データを更新しました！', 'success');
                
            } catch (error) {
                console.error('Correction error:', error);
                this.showNotification('❌ 更新に失敗しました', 'error');
            }
        }
    }
    
    handleAccept() {
        this.showNotification('✅ フィードバックありがとうございます！', 'success');
    }
    
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `companygenius-notification companygenius-notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        requestAnimationFrame(() => {
            notification.classList.add('show');
        });
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    removePredictionDialog() {
        if (this.currentDialog) {
            this.currentDialog.classList.remove('show');
            setTimeout(() => {
                if (this.currentDialog && this.currentDialog.parentNode) {
                    this.currentDialog.parentNode.removeChild(this.currentDialog);
                }
                this.currentDialog = null;
            }, 300);
        }
    }
    
    addDialogStyles() {
        // スタイルが既に追加されていれば何もしない
        if (document.getElementById('companygenius-styles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'companygenius-styles';
        styles.textContent = `
            .companygenius-dialog {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .companygenius-dialog.show {
                opacity: 1;
            }
            
            .companygenius-dialog-content {
                background: white;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                max-width: 400px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                transform: scale(0.9);
                transition: transform 0.3s ease;
            }
            
            .companygenius-dialog.show .companygenius-dialog-content {
                transform: scale(1);
            }
            
            .companygenius-header {
                display: flex;
                align-items: center;
                padding: 16px 20px;
                border-bottom: 1px solid #eee;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 12px 12px 0 0;
            }
            
            .companygenius-icon {
                font-size: 20px;
                margin-right: 8px;
            }
            
            .companygenius-title {
                font-weight: 600;
                flex: 1;
            }
            
            .companygenius-close {
                background: none;
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: background 0.2s ease;
            }
            
            .companygenius-close:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            
            .companygenius-body {
                padding: 20px;
                color: #333;
            }
            
            .companygenius-query {
                margin-bottom: 16px;
                font-size: 14px;
                color: #666;
            }
            
            .companygenius-result {
                margin-bottom: 16px;
            }
            
            .companygenius-company-name {
                font-size: 18px;
                font-weight: 700;
                color: #333;
                margin-bottom: 8px;
                padding: 12px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            
            .companygenius-details {
                font-size: 13px;
                color: #666;
            }
            
            .companygenius-details div {
                margin-bottom: 4px;
            }
            
            .companygenius-alternatives {
                margin-bottom: 16px;
                padding: 12px;
                background: #f1f3f4;
                border-radius: 8px;
            }
            
            .companygenius-alternatives-title {
                font-size: 12px;
                font-weight: 600;
                margin-bottom: 8px;
                color: #5f6368;
            }
            
            .companygenius-alternative {
                font-size: 12px;
                color: #666;
                margin-bottom: 4px;
                padding-left: 8px;
            }
            
            .companygenius-actions {
                display: flex;
                gap: 8px;
                margin-bottom: 16px;
            }
            
            .companygenius-btn {
                flex: 1;
                padding: 10px 16px;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .companygenius-correct-btn {
                background: #ff6b6b;
                color: white;
            }
            
            .companygenius-correct-btn:hover {
                background: #ff5252;
            }
            
            .companygenius-accept-btn {
                background: #51cf66;
                color: white;
            }
            
            .companygenius-accept-btn:hover {
                background: #40c057;
            }
            
            .companygenius-note {
                font-size: 12px;
                color: #666;
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 6px;
                padding: 8px;
            }
            
            .companygenius-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                border-radius: 8px;
                padding: 12px 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
                z-index: 10001;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                font-size: 14px;
                opacity: 0;
                transform: translateX(100%);
                transition: all 0.3s ease;
            }
            
            .companygenius-notification.show {
                opacity: 1;
                transform: translateX(0);
            }
            
            .companygenius-notification-success {
                border-left: 4px solid #51cf66;
            }
            
            .companygenius-notification-error {
                border-left: 4px solid #ff6b6b;
            }
        `;
        
        document.head.appendChild(styles);
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

// コンテンツスクリプト初期化
new EmbeddedContent();

console.log('🔗 CompanyGenius Embedded content script initialized');