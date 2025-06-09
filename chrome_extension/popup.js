// Phase 15 - Simple Popup Script

// Global function for handling incorrect prediction clicks
window.handleIncorrectClick = function(query, predictedName) {
    console.log('Global incorrect handler called:', query, predictedName);
    showCorrectionDialog(query, predictedName);
};

// Add a global test function
window.testIncorrectButton = function() {
    console.log('Testing incorrect button functionality...');
    showCorrectionDialog('テスト', '株式会社テスト');
};

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const predictBtn = document.getElementById('predictBtn');
    const resultDiv = document.getElementById('result');
    const viewCorrectionsBtn = document.getElementById('viewCorrectionsBtn');
    
    // Add event delegation for dynamically created buttons (multiple approaches for reliability)
    document.addEventListener('click', function(e) {
        // Handle incorrectBtn by ID
        if (e.target && e.target.id === 'incorrectBtn') {
            console.log('Incorrect button clicked via delegation!');
            e.preventDefault();
            e.stopPropagation();
            
            // Get stored data from button attributes
            const query = e.target.getAttribute('data-query');
            const predictedName = e.target.getAttribute('data-predicted');
            console.log('Popup data from button:', query, predictedName);
            
            if (query && predictedName) {
                showCorrectionDialog(query, predictedName);
            } else {
                console.log('Missing data attributes on button');
            }
            return;
        }
        
        // Handle incorrectBtn by class (backup method)
        if (e.target && e.target.classList.contains('incorrect-btn')) {
            console.log('Incorrect button clicked via class delegation!');
            e.preventDefault();
            e.stopPropagation();
            
            const query = e.target.getAttribute('data-query');
            const predictedName = e.target.getAttribute('data-predicted');
            console.log('Popup data from class button:', query, predictedName);
            
            if (query && predictedName) {
                showCorrectionDialog(query, predictedName);
            }
            return;
        }
    });
    
    // Test connection on load
    testConnection();
    
    // Predict button handler
    if (predictBtn) {
        predictBtn.addEventListener('click', function() {
            const query = searchInput.value.trim();
            if (query) {
                predict(query);
            }
        });
    }
    
    // Enter key handler
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const query = searchInput.value.trim();
                if (query) {
                    predict(query);
                }
            }
        });
    }
    
    // View corrections button handler
    if (viewCorrectionsBtn) {
        viewCorrectionsBtn.addEventListener('click', function() {
            viewSavedCorrections();
        });
    }
});

// Prediction function
async function predict(query) {
    const resultDiv = document.getElementById('result');
    if (!resultDiv) return;
    
    resultDiv.innerHTML = '<div>予測中...</div>';
    
    try {
        const response = await chrome.runtime.sendMessage({
            action: 'predict',
            query: query
        });
        
        if (response.error) {
            resultDiv.innerHTML = `<div style="color: red;">エラー: ${response.error}</div>`;
        } else {
            const confidence = (response.confidence * 100).toFixed(1);
            resultDiv.innerHTML = `
                <div style="padding: 10px; background: #f0f0f0; border-radius: 5px;">
                    <strong>予測結果:</strong><br>
                    ${response.predicted_name}<br>
                    <small>信頼度: ${confidence}% | ソース: ${response.source}</small><br>
                    <div style="margin-top: 8px; display: flex; gap: 5px;">
                        <button id="copyResult" style="flex: 1; padding: 6px 10px; background: #4CAF50; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 12px; min-height: 28px;">📋 コピー</button>
                        <button id="incorrectBtn" class="incorrect-btn" data-query="${query}" data-predicted="${response.predicted_name}" style="flex: 1; padding: 6px 10px; background: #FF9800; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 12px; min-height: 28px;">❌ 間違い</button>
                    </div>
                </div>
            `;
            
            console.log('Result HTML set, buttons should be available now');
            
            // Add copy functionality
            const copyBtn = document.getElementById('copyResult');
            if (copyBtn) {
                copyBtn.addEventListener('click', async () => {
                    try {
                        await navigator.clipboard.writeText(response.predicted_name);
                        copyBtn.textContent = '✅ コピー済み!';
                        setTimeout(() => {
                            copyBtn.textContent = '📋 コピー';
                        }, 1500);
                    } catch (error) {
                        // Fallback method
                        const textArea = document.createElement('textarea');
                        textArea.value = response.predicted_name;
                        textArea.style.position = 'fixed';
                        textArea.style.left = '-999999px';
                        document.body.appendChild(textArea);
                        textArea.focus();
                        textArea.select();
                        document.execCommand('copy');
                        document.body.removeChild(textArea);
                        copyBtn.textContent = '✅ コピー済み!';
                        setTimeout(() => {
                            copyBtn.textContent = '📋 コピー';
                        }, 1500);
                    }
                });
            }
            
            // Event delegation handles the incorrect button click
            console.log('Buttons created with event delegation support');
        }
    } catch (error) {
        resultDiv.innerHTML = `<div style="color: red;">通信エラー: ${error.message}</div>`;
    }
}

// Test API connection
async function testConnection() {
    const statusDiv = document.getElementById('status');
    if (!statusDiv) return;
    
    try {
        const response = await chrome.runtime.sendMessage({
            action: 'testConnection'
        });
        
        if (response.error) {
            statusDiv.innerHTML = '🔴 API接続エラー';
            statusDiv.style.color = 'red';
        } else {
            statusDiv.innerHTML = '🟢 API接続正常';
            statusDiv.style.color = 'green';
        }
    } catch (error) {
        statusDiv.innerHTML = '🔴 接続失敗';
        statusDiv.style.color = 'red';
    }
}

// Show correction dialog for incorrect predictions  
function showCorrectionDialog(originalQuery, predictedName) {
    console.log(`Opening correction dialog for: ${originalQuery} -> ${predictedName}`);
    
    const resultDiv = document.getElementById('result');
    if (!resultDiv) return;
    
    resultDiv.innerHTML = `
        <div style="padding: 10px; background: #fff3cd; border: 1px solid #ffc107; border-radius: 5px;">
            <h4 style="margin: 0 0 10px 0; color: #856404;">🔧 予測を修正</h4>
            <div style="margin-bottom: 10px;">
                <strong>検索:</strong> ${originalQuery}<br>
                <strong>予測:</strong> ${predictedName}
            </div>
            <div style="margin-bottom: 10px;">
                <label style="display: block; margin-bottom: 5px; font-weight: bold;">正しい企業名:</label>
                <input type="text" id="correctName" placeholder="例: 株式会社○○" 
                       style="width: 100%; padding: 5px; border: 1px solid #ccc; border-radius: 3px; box-sizing: border-box;">
            </div>
            <div style="display: flex; gap: 5px;">
                <button id="submitCorrection" style="flex: 1; padding: 6px 12px; background: #28a745; color: white; border: none; border-radius: 3px; cursor: pointer;">✅ 修正を送信</button>
                <button id="cancelCorrection" style="flex: 1; padding: 6px 12px; background: #6c757d; color: white; border: none; border-radius: 3px; cursor: pointer;">❌ キャンセル</button>
            </div>
        </div>
    `;
    
    // Focus on the input field
    const correctNameInput = document.getElementById('correctName');
    if (correctNameInput) {
        correctNameInput.focus();
    }
    
    // Add submit functionality
    const submitBtn = document.getElementById('submitCorrection');
    if (submitBtn) {
        submitBtn.addEventListener('click', async () => {
            const correctName = correctNameInput.value.trim();
            if (correctName) {
                await submitCorrection(originalQuery, predictedName, correctName);
            } else {
                alert('正しい企業名を入力してください。');
            }
        });
    }
    
    // Add cancel functionality
    const cancelBtn = document.getElementById('cancelCorrection');
    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
            resultDiv.innerHTML = '<div>予測結果がキャンセルされました。</div>';
        });
    }
    
    // Enter key handler for input
    if (correctNameInput) {
        correctNameInput.addEventListener('keypress', async (e) => {
            if (e.key === 'Enter') {
                const correctName = correctNameInput.value.trim();
                if (correctName) {
                    await submitCorrection(originalQuery, predictedName, correctName);
                }
            }
        });
    }
}

// Submit correction to API
async function submitCorrection(originalQuery, predictedName, correctName) {
    const resultDiv = document.getElementById('result');
    if (!resultDiv) return;
    
    resultDiv.innerHTML = '<div>修正を送信中...</div>';
    
    try {
        const response = await chrome.runtime.sendMessage({
            action: 'submitCorrection',
            originalQuery: originalQuery,
            predictedName: predictedName,
            correctName: correctName
        });
        
        if (response.error) {
            resultDiv.innerHTML = `<div style="color: red;">修正送信エラー: ${response.error}</div>`;
        } else {
            resultDiv.innerHTML = `
                <div style="padding: 10px; background: #d4edda; border: 1px solid #c3e6cb; border-radius: 5px; color: #155724;">
                    <strong>✅ 修正が送信されました</strong><br>
                    検索: ${originalQuery}<br>
                    修正前: ${predictedName}<br>
                    修正後: ${correctName}<br>
                    <small>この修正は今後の予測精度向上に使用されます。</small>
                </div>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div style="color: red;">通信エラー: ${error.message}</div>`;
    }
}
// View saved corrections function
function viewSavedCorrections() {
    const resultDiv = document.getElementById("result");
    if (\!resultDiv) return;
    
    try {
        const corrections = JSON.parse(localStorage.getItem("phase15_corrections") || "[]");
        
        if (corrections.length === 0) {
            resultDiv.innerHTML = `
                <div style="padding: 10px; background: #f0f0f0; border-radius: 5px;">
                    <strong>保存された修正:</strong><br>
                    まだ修正データがありません。
                </div>
            `;
            return;
        }
        
        let html = `
            <div style="padding: 10px; background: #f0f0f0; border-radius: 5px;">
                <strong>保存された修正 (${corrections.length}件):</strong><br>
                <div style="max-height: 200px; overflow-y: auto; margin-top: 10px;">
        `;
        
        corrections.forEach((correction, index) => {
            const status = correction.status === "synced_to_server" ? 
                "<span style=\"color: green;\">✅ 同期済み</span>" : 
                "<span style=\"color: orange;\">📱 ローカル保存</span>";
            
            html += `
                <div style="margin: 5px 0; padding: 8px; background: white; border-radius: 3px; font-size: 12px;">
                    <strong>${correction.original_query}</strong><br>
                    ${correction.predicted_name} → ${correction.correct_name}<br>
                    <small>${new Date(correction.timestamp).toLocaleString()}  < /dev/null |  ${status}</small>
                </div>
            `;
        });
        
        html += `
                </div>
                <button onclick="clearCorrections()" style="margin-top: 10px; padding: 4px 8px; background: #dc3545; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 12px;">全て削除</button>
            </div>
        `;
        
        resultDiv.innerHTML = html;
        
    } catch (error) {
        resultDiv.innerHTML = `<div style="color: red;">修正データの読み込みに失敗しました: ${error.message}</div>`;
    }
}

// Clear corrections function
window.clearCorrections = function() {
    if (confirm("保存された修正データを全て削除しますか？")) {
        localStorage.removeItem("phase15_corrections");
        viewSavedCorrections(); // Refresh view
    }
};
