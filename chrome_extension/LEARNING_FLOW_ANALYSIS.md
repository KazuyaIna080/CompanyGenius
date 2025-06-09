# 🔄 学習機能フロー分析

## 現在の動作フロー

### 1. 右クリック予測の流れ
```
ユーザー操作: テキスト選択 → 右クリック → 「企業名を予測」
    ↓
background.js: chrome.contextMenus.onClicked.addListener()
    ↓
background.js: handlePrediction(info.selectionText)
    ↓
background.js: fetch('http://localhost:8001/predict?q=企業名')
    ↓
API Server: phase15_fixed_api.py の handle_prediction()
    ↓
Prediction System: phase15_final_system.py の cascade_predict()
    ↓
Level 1: level1_user_learning() - ユーザー修正データ検索
    ↓
Level 2: level2_edinet_listed() - EDINET上場企業
    ↓
Level 5: level5_brand_mapping() - ブランドマッピング
    ↓
Level 7: level7_ml_fallback() - MLフォールバック
    ↓
結果をJSON形式で返却
    ↓
background.js: showPredictionDialog() で表示
```

### 2. 修正送信の流れ
```
ユーザー操作: 「❌ 間違い」ボタンクリック
    ↓
background.js: window.handleIncorrectClick()
    ↓
修正ダイアログ表示 → ユーザーが正しい企業名入力
    ↓
background.js: 修正送信ボタンクリック
    ↓
background.js: window.postMessage() で修正データ送信
    ↓
content.js: window.addEventListener('message')
    ↓
content.js: chrome.runtime.sendMessage() でbackground.jsに転送
    ↓
background.js: chrome.runtime.onMessage.addListener()
    ↓
background.js: handleCorrection()
    ↓
background.js: fetch('http://localhost:8001/correction', POST)
    ↓
API Server: phase15_fixed_api.py の handle_correction()
    ↓
Prediction System: add_user_correction() でメモリ内キャッシュに保存
    ↓
corrections.logファイルに追記
    ↓
成功レスポンスを返却
```

## 🚨 問題点の特定

### Issue 1: メモリ内学習データの揮発性
```python
# phase15_final_system.py
def __init__(self):
    self.user_corrections = {}  # ← これはメモリ内のみ
    self._load_user_corrections()  # ← 起動時のみ読み込み

def add_user_correction(self, original_query, predicted_name, correct_name):
    # メモリ内には保存されるが...
    self.user_corrections[normalized_query] = {...}
    # ファイルへの書き込みは corrections.log のみ
```

### Issue 2: 新しい予測時にメモリデータが使われない
- API予測リクエストのたびに新しいシステムインスタンスが作成される可能性
- または、既存インスタンスのメモリデータが更新されていない

### Issue 3: ファイル書き込みとメモリ同期の不整合
```python
# corrections.log に書き込み
with open(correction_log, 'a', encoding='utf-8') as f:
    f.write(json.dumps(correction_entry, ensure_ascii=False) + '\n')

# しかし、現在のインスタンスのメモリには即座に反映されない可能性
```

## 🔍 検証が必要な項目

### A. APIサーバーでの学習データ状態確認
1. 修正送信後に `self.user_corrections` の内容をログ出力
2. 次の予測時に `level1_user_learning()` が正しく呼ばれているか確認
3. 同一インスタンスが使われているか、新しいインスタンスが作成されているか確認

### B. ファイル保存と読み込みの確認
1. `corrections.log` にデータが正しく書き込まれているか
2. `_load_user_corrections()` が正しく動作しているか
3. メモリ内データとファイルデータの同期状態

### C. 正規化処理の確認
1. 検索時の `_normalize_query()` と保存時の正規化が一致しているか
2. 大文字小文字、記号、スペースの処理が統一されているか

## 🛠️ 修正アプローチ

### Step 1: デバッグ情報の追加
- APIサーバーに詳細なログ出力を追加
- 学習データの状態を可視化

### Step 2: リアルタイム学習の確実な実装
- 修正データ受信時に即座にメモリ内データを更新
- ファイル書き込みとメモリ更新を同期

### Step 3: 学習データの永続化改善
- 予測システムの単一インスタンス化
- または、リクエストのたびにファイルから最新データを読み込み

## 🎯 次の対応優先順位

1. **高優先度**: APIサーバーでのデバッグログ追加
2. **中優先度**: 学習データの即座反映機能実装
3. **低優先度**: ファイル読み込み最適化

---

## 予想される根本原因

**メモリ内学習データが次の予測リクエスト時に利用されていない**
- APIサーバーで新しいシステムインスタンスが作成されている
- または既存インスタンスのメモリデータが更新されていない