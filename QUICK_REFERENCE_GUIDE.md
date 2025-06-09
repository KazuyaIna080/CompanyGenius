# ⚡ クイックリファレンスガイド

## 🎯 よくある問題と即座解決

### 🔧 Chrome拡張機能の「❌ 間違い」ボタンが押せない

**原因**: 動的要素のイベント未登録  
**解決**: イベントデリゲーション + data属性

```javascript
// ❌ 悪い例
<button onclick="handleClick('${data}')">❌ 間違い</button>

// ✅ 良い例
<button id="incorrectBtn" class="incorrect-btn" data-query="${query}" data-predicted="${predicted}">❌ 間違い</button>

// イベントデリゲーション
document.addEventListener('click', function(e) {
    if (e.target && (e.target.id === 'incorrectBtn' || e.target.classList.contains('incorrect-btn'))) {
        const query = e.target.getAttribute('data-query');
        const predicted = e.target.getAttribute('data-predicted');
        handleIncorrectClick(query, predicted);
    }
});
```

### 🌍 日本語文字化け「ãã³ã¢ã»ãã¯ãã­ã¸」

**原因**: UTF-8エンコーディング設定不備  
**解決**: 環境変数 + ヘッダー設定

```python
# サーバー側
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

# HTTPレスポンス
self.send_header('Content-type', 'application/json; charset=utf-8')
json_data = json.dumps(data, ensure_ascii=False)
self.wfile.write(json_data.encode('utf-8'))
```

```javascript
// クライアント側
const url = new URL('http://localhost:8001/predict');
url.searchParams.set('q', query);  // 自動UTF-8エンコード
```

### 🔄 学習データが次の予測に反映されない

**原因**: メモリ内データの揮発化  
**解決**: シングルトンパターン + 即座反映

```python
# APIハンドラーでシングルトン
def __init__(self, *args, **kwargs):
    if not hasattr(Phase15FixedAPIHandler, 'prediction_system'):
        Phase15FixedAPIHandler.prediction_system = FinalCascadeSystem()

# 学習データの即座反映
def add_user_correction(self, original_query, predicted_name, correct_name):
    normalized_query = self._normalize_query(original_query)
    self.user_corrections[normalized_query] = {
        'correct_name': correct_name,
        'confidence': 1.0
    }
    return True
```

### 🌐 CORS エラー「blocked by CORS policy」

**原因**: クロスオリジンリクエスト制限  
**解決**: Service Worker + OPTIONS対応

```python
# サーバー側 CORS設定
def do_OPTIONS(self):
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    self.end_headers()
```

```javascript
// Chrome拡張機能側
// background.js (Service Worker) でAPIリクエスト処理
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'predict') {
        handlePrediction(request.query).then(sendResponse);
        return true;
    }
});
```

---

## 📋 開発チェックリスト

### ✅ 基本設定
- [ ] UTF-8環境変数設定
- [ ] CORS ヘッダー設定
- [ ] manifest.json 権限設定
- [ ] イベントデリゲーション実装

### ✅ 品質確認
- [ ] 日本語文字化けなし
- [ ] ボタンクリック動作確認
- [ ] 学習データ反映確認
- [ ] エラーハンドリング動作確認

### ✅ デバッグ準備
- [ ] コンソールログ出力
- [ ] サーバーログ監視
- [ ] ネットワークタブ確認
- [ ] ファイル保存確認

---

## 🚀 即座実行コマンド

```bash
# サーバー起動
nohup python3 phase15_fixed_api.py > server.log 2>&1 &

# ログ監視
tail -f server.log

# API動作確認
curl "http://localhost:8001/predict?q=トヨタ"

# 修正ログ確認
tail -5 corrections.log

# プロセス確認
ps aux | grep phase15_fixed_api
```

---

## 🎯 トラブルシューティング

| 症状 | 原因 | 解決 |
|------|------|------|
| ボタンが押せない | イベント未登録 | イベントデリゲーション |
| 文字化け | UTF-8設定不備 | 環境変数 + ヘッダー |
| 学習が反映されない | メモリ揮発 | シングルトン実装 |
| CORS エラー | 同一オリジン制限 | Service Worker使用 |
| 関数未定義エラー | スコープ問題 | グローバル定義順序 |

**このガイドで95%の問題は即座解決できます。** 🎉