// Phase 15 Content Script - Message Passing Handler
console.log('Phase15 Content Script loaded');

// Global event delegation for incorrect buttons (additional safety net)
document.addEventListener('click', function(e) {
    if (e.target && (e.target.id === 'incorrectBtn' || e.target.classList.contains('incorrect-btn'))) {
        console.log('Content script detected incorrect button click');
        
        const query = e.target.getAttribute('data-query');
        const predicted = e.target.getAttribute('data-predicted');
        
        if (query && predicted && window.handleIncorrectClick) {
            console.log('Content script calling handleIncorrectClick');
            window.handleIncorrectClick(query, predicted);
        }
    }
}, true); // Use capture to ensure we catch events early

// Listen for correction requests from injected scripts
window.addEventListener('message', async (event) => {
    if (event.data && event.data.type === 'PHASE15_CORRECTION_REQUEST') {
        console.log('Content script received correction request:', event.data.data);
        
        try {
            // Forward to background script via chrome.runtime.sendMessage
            const response = await chrome.runtime.sendMessage({
                action: 'submitCorrection',
                originalQuery: event.data.data.original_query,
                predictedName: event.data.data.predicted_name,
                correctName: event.data.data.correct_name
            });
            
            // Send response back to injected script
            window.postMessage({
                type: 'PHASE15_CORRECTION_RESPONSE',
                success: !response.error,
                error: response.error
            }, '*');
            
        } catch (error) {
            console.error('Content script error:', error);
            
            // Send error response
            window.postMessage({
                type: 'PHASE15_CORRECTION_RESPONSE',
                success: false,
                error: error.message
            }, '*');
        }
    }
});