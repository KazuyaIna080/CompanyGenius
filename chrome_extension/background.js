// Phase 15 - Minimal Service Worker
console.log('Service Worker loaded');

// Installation handler
chrome.runtime.onInstalled.addListener(() => {
    console.log('Extension installed');
    
    // Create context menu
    chrome.contextMenus.create({
        id: 'predict-company',
        title: 'CompanyGenius で企業名を予測',
        contexts: ['selection']
    });
});

// Message handler for popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'predict') {
        handlePrediction(request.query).then(sendResponse);
        return true; // Keep message channel open
    }
    
    if (request.action === 'testConnection') {
        testConnection().then(sendResponse);
        return true;
    }
    
    if (request.action === 'submitCorrection') {
        handleCorrection(request.originalQuery, request.predictedName, request.correctName).then(sendResponse);
        return true;
    }
});

// Context menu click handler
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
    if (info.menuItemId === 'predict-company' && info.selectionText) {
        try {
            console.log('Context menu clicked, selected text:', info.selectionText);
            
            // Make prediction in background script (no CORS issues)
            const result = await handlePrediction(info.selectionText);
            console.log('Prediction result:', result);
            
            // Inject script to show result
            await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                func: showPredictionDialog,
                args: [result]
            });
            
            console.log('Dialog script injected successfully');
            
        } catch (error) {
            console.error('Context menu error:', error);
            
            // Show error dialog
            try {
                await chrome.scripting.executeScript({
                    target: { tabId: tab.id },
                    func: showErrorDialog,
                    args: [error.message]
                });
            } catch (injectError) {
                console.error('Failed to inject error dialog:', injectError);
            }
        }
    }
});

// Function to show prediction dialog (injected into page)
function showPredictionDialog(result) {
    console.log('Creating prediction dialog for:', result);
    
    // Remove existing dialogs
    const existing = document.getElementById('phase15-dialog');
    if (existing) existing.remove();
    const existingCorrection = document.getElementById('phase15-correction-dialog');
    if (existingCorrection) existingCorrection.remove();
    
    // Create dialog
    const dialog = document.createElement('div');
    dialog.id = 'phase15-dialog';
    dialog.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        width: 320px;
        background: white;
        border: 2px solid #4CAF50;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        font-family: Arial, sans-serif;
        font-size: 14px;
        padding: 16px;
    `;
    
    // Confidence color
    let confidenceColor = '#4CAF50';
    if (result.confidence < 0.8) confidenceColor = '#FF9800';
    if (result.confidence < 0.6) confidenceColor = '#F44336';
    
    dialog.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <h3 style="margin: 0; color: #4CAF50;">🧠 CompanyGenius</h3>
            <button onclick="this.parentElement.remove()" style="background: none; border: none; font-size: 18px; cursor: pointer;">×</button>
        </div>
        
        <div style="margin-bottom: 12px;">
            <strong>検索:</strong> "${result.query}"
        </div>
        
        <div style="margin-bottom: 12px; padding: 12px; background: #f0f8f0; border-radius: 4px;">
            <div style="font-size: 16px; font-weight: bold; color: #333;">
                ${result.predicted_name}
            </div>
            <div style="margin-top: 4px;">
                <span style="color: ${confidenceColor}; font-weight: bold;">
                    信頼度: ${(result.confidence * 100).toFixed(1)}%
                </span>
                <span style="margin-left: 8px; color: #666; font-size: 12px;">
                    ソース: ${result.source}
                </span>
            </div>
        </div>
        
        <div style="display: flex; gap: 8px;">
            <button id="copyBtn" style="flex: 1; padding: 6px 12px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
                📋 コピー
            </button>
            <button id="incorrectBtn" class="incorrect-btn" data-query="${result.query}" data-predicted="${result.predicted_name}" style="flex: 1; padding: 6px 12px; background: #FF9800; color: white; border: none; border-radius: 4px; cursor: pointer;">
                ❌ 間違い
            </button>
        </div>
    `;
    
    // Define global handler function FIRST (before creating dialog)
    window.handleIncorrectClick = function(query, predictedName) {
        console.log('Incorrect button clicked with:', query, predictedName);
        console.log('Data received - Query:', query, 'PredictedName:', predictedName);
        
        // Remove existing dialogs
        const existing = document.getElementById('phase15-dialog');
        if (existing) existing.remove();
        const existingCorrection = document.getElementById('phase15-correction-dialog');
        if (existingCorrection) existingCorrection.remove();
        
        // Show correction dialog
        const correctionDialog = document.createElement('div');
        correctionDialog.id = 'phase15-correction-dialog';
        correctionDialog.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            width: 350px;
            background: white;
            border: 2px solid #FF9800;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10002;
            font-family: Arial, sans-serif;
            font-size: 14px;
            padding: 16px;
        `;
        
        correctionDialog.innerHTML = `
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
                <h3 style='margin: 0; color: #FF9800;'>🔧 予測を修正</h3>
                <button onclick='this.parentElement.parentElement.remove()' style='background: none; border: none; font-size: 18px; cursor: pointer;'>×</button>
            </div>
            
            <div style='margin-bottom: 12px; font-size: 12px; color: #666;'>
                <strong>検索:</strong> ${query}<br>
                <strong>予測:</strong> ${predictedName}
            </div>
            
            <div style='margin-bottom: 12px;'>
                <label style='display: block; margin-bottom: 5px; font-weight: bold;'>正しい企業名:</label>
                <input type='text' id='correctNameInput' placeholder='例: 株式会社○○' 
                       style='width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 14px;'>
            </div>
            
            <div style='display: flex; gap: 8px;'>
                <button id='submitCorrectionBtn' style='flex: 1; padding: 8px 12px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;'>
                    ✅ 修正を送信
                </button>
                <button onclick='this.parentElement.parentElement.remove()' style='flex: 1; padding: 8px 12px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;'>
                    ❌ キャンセル
                </button>
            </div>
            
            <div id='correctionStatus' style='margin-top: 10px; font-size: 12px;'></div>
        `;
        
        document.body.appendChild(correctionDialog);
        
        // Focus on input
        setTimeout(() => {
            const input = document.getElementById('correctNameInput');
            if (input) input.focus();
        }, 100);
        
        // Add submit functionality using event listener (more reliable than onclick)
        const submitBtn = document.getElementById('submitCorrectionBtn');
        if (submitBtn) {
            submitBtn.addEventListener('click', function() {
                const input = document.getElementById('correctNameInput');
                const status = document.getElementById('correctionStatus');
                const correctName = input ? input.value.trim() : '';
                
                if (!correctName) {
                    status.innerHTML = '<span style="color: red;">正しい企業名を入力してください。</span>';
                    return;
                }
                
                status.innerHTML = '<span style="color: blue;">修正を送信中...</span>';
                
                window.postMessage({
                    type: 'PHASE15_CORRECTION_REQUEST',
                    data: {
                        original_query: query,
                        predicted_name: predictedName,
                        correct_name: correctName,
                        timestamp: new Date().toISOString(),
                        source: 'chrome_extension_content'
                    }
                }, '*');
                
                const messageHandler = (event) => {
                    if (event.data && event.data.type === 'PHASE15_CORRECTION_RESPONSE') {
                        window.removeEventListener('message', messageHandler);
                        
                        if (event.data.success) {
                            status.innerHTML = '<span style="color: green;">✅ 修正が保存されました</span>';
                        } else {
                            status.innerHTML = '<span style="color: orange;">⚠️ ローカルに保存されました</span>';
                        }
                        
                        setTimeout(() => {
                            correctionDialog.remove();
                        }, 2000);
                    }
                };
                
                window.addEventListener('message', messageHandler);
                
                setTimeout(() => {
                    window.removeEventListener('message', messageHandler);
                    status.innerHTML = '<span style="color: orange;">⚠️ ローカルに保存されました</span>';
                    setTimeout(() => {
                        correctionDialog.remove();
                    }, 2000);
                }, 3000);
            });
        }
    };
    
    document.body.appendChild(dialog);
    
    // Add copy functionality
    const copyBtn = dialog.querySelector('#copyBtn');
    if (copyBtn) {
        copyBtn.addEventListener('click', async () => {
            try {
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    await navigator.clipboard.writeText(result.predicted_name);
                    copyBtn.textContent = '✅ コピー済み!';
                } else {
                    // Fallback method
                    const textArea = document.createElement('textarea');
                    textArea.value = result.predicted_name;
                    textArea.style.position = 'fixed';
                    textArea.style.left = '-999999px';
                    document.body.appendChild(textArea);
                    textArea.focus();
                    textArea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textArea);
                    copyBtn.textContent = '✅ コピー済み!';
                }
                
                setTimeout(() => {
                    copyBtn.textContent = '📋 コピー';
                }, 1500);
                
            } catch (error) {
                console.error('Copy failed:', error);
                copyBtn.textContent = '❌ コピー失敗';
                setTimeout(() => {
                    copyBtn.textContent = '📋 コピー';
                }, 1500);
            }
        });
    }
    
    // Add incorrect button functionality using event listener (more reliable)
    const incorrectBtn = dialog.querySelector('#incorrectBtn');
    if (incorrectBtn) {
        incorrectBtn.addEventListener('click', function() {
            const query = this.getAttribute('data-query');
            const predicted = this.getAttribute('data-predicted');
            console.log('Right-click data from button:', query, predicted);
            
            if (window.handleIncorrectClick) {
                window.handleIncorrectClick(query, predicted);
            } else {
                console.error('handleIncorrectClick function not available');
            }
        });
    }
    
    // Add additional event delegation for right-click context (backup method)
    document.addEventListener('click', function(e) {
        if (e.target && (e.target.id === 'incorrectBtn' || e.target.classList.contains('incorrect-btn'))) {
            console.log('Right-click incorrect button clicked via delegation!');
            
            const query = e.target.getAttribute('data-query');
            const predicted = e.target.getAttribute('data-predicted');
            console.log('Right-click data from button:', query, predicted);
            
            if (query && predicted) {
                // Call the correct handler function
                if (window.handleIncorrectClick) {
                    window.handleIncorrectClick(query, predicted);
                } else {
                    console.error('handleIncorrectClick function not available, creating correction dialog directly');
                    // Fallback: call the correction dialog directly
                    if (window.showCorrectionDialog) {
                        window.showCorrectionDialog(query, predicted);
                    } else {
                        // Last resort: create minimal correction interface
                        window.handleIncorrectClick(query, predicted);
                    }
                }
            }
            e.preventDefault();
            e.stopPropagation();
        }
    }, true);
    
    // Auto-remove after 8 seconds
    setTimeout(() => {
        if (document.getElementById('phase15-dialog')) {
            dialog.remove();
        }
    }, 8000);
}

// Error dialog function (injected into page)
function showErrorDialog(errorMessage) {
    // Remove existing dialogs
    const existing = document.getElementById('phase15-dialog');
    if (existing) existing.remove();
    
    // Create error dialog
    const errorDialog = document.createElement('div');
    errorDialog.id = 'phase15-dialog';
    errorDialog.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        width: 320px;
        background: white;
        border: 2px solid #F44336;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        font-family: Arial, sans-serif;
        font-size: 14px;
        padding: 16px;
    `;
    
    errorDialog.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <h3 style="margin: 0; color: #F44336;">❌ エラー</h3>
            <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; font-size: 18px; cursor: pointer;">×</button>
        </div>
        
        <div style="margin-bottom: 12px; color: #333;">
            予測の取得に失敗しました:<br>
            <small style="color: #666;">${errorMessage}</small>
        </div>
        
        <div style="display: flex; gap: 8px;">
            <button onclick="this.parentElement.parentElement.remove()" style="flex: 1; padding: 6px 12px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">
                閉じる
            </button>
        </div>
    `;
    
    document.body.appendChild(errorDialog);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (document.getElementById('phase15-dialog')) {
            errorDialog.remove();
        }
    }, 5000);
}

// API prediction function
async function handlePrediction(query) {
    try {
        console.log('Making prediction request for:', query);
        
        // Create proper UTF-8 encoded URL
        const url = new URL('http://localhost:8001/predict');
        url.searchParams.set('q', query);
        
        const response = await fetch(url.toString());
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        result.query = query; // Ensure original query is preserved
        return result;
    } catch (error) {
        console.error('Prediction error:', error);
        return {
            error: error.message,
            query: query,
            predicted_name: `株式会社${query}`,
            confidence: 0.5,
            source: 'fallback'
        };
    }
}

// Test API connection
async function testConnection() {
    try {
        const response = await fetch('http://localhost:8001/health');
        if (response.ok) {
            return { status: 'connected' };
        }
        throw new Error('Connection failed');
    } catch (error) {
        return { error: error.message };
    }
}

// Handle correction submission
async function handleCorrection(originalQuery, predictedName, correctName) {
    try {
        console.log(`🔧 Correction submission: "${originalQuery}" -> "${correctName}"`);
        
        const response = await fetch('http://localhost:8001/correction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json; charset=utf-8'
            },
            body: JSON.stringify({
                original_query: originalQuery,
                predicted_name: predictedName,
                correct_name: correctName,
                timestamp: new Date().toISOString(),
                source: 'chrome_extension'
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        console.log('✅ Correction submitted successfully');
        
        return {
            success: true,
            message: 'Correction submitted successfully',
            result: result
        };
        
    } catch (error) {
        console.error('❌ Correction submission error:', error);
        
        // Fallback: Store correction locally
        try {
            const corrections = await chrome.storage.local.get('corrections') || { corrections: [] };
            corrections.corrections = corrections.corrections || [];
            corrections.corrections.push({
                original_query: originalQuery,
                predicted_name: predictedName,
                correct_name: correctName,
                timestamp: new Date().toISOString(),
                status: 'pending_sync'
            });
            
            await chrome.storage.local.set(corrections);
            
            return {
                success: true,
                message: 'Correction saved locally (will sync when server is available)',
                fallback: true
            };
        } catch (storageError) {
            return {
                error: `Failed to save correction: ${error.message}`,
                fallback_error: storageError.message
            };
        }
    }
}