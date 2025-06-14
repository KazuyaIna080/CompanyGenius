# Chrome Extension Testing Guide

## 拡張機能の再読み込み手順

1. Chrome で `chrome://extensions/` を開く
2. "Phase 15 Enterprise Name Prediction" 拡張機能を見つける
3. "再読み込み" ボタンをクリック
4. 拡張機能が正しく読み込まれたことを確認

## テスト手順

### ポップアップテスト
1. 拡張機能アイコンをクリック
2. 検索ボックスに企業名を入力（例：「トヨタ」）
3. 「予測」ボタンをクリック
4. 結果が表示されたら「❌ 間違い」ボタンをクリック
5. 修正ダイアログが表示されることを確認

### 右クリックメニューテスト
1. ウェブページで企業名テキストを選択（例：「ソニー」）
2. 右クリックして「企業名を予測」を選択
3. 予測ダイアログが表示されたら「❌ 間違い」ボタンをクリック
4. 修正ダイアログが表示されることを確認

## デバッグ方法

### コンソールログ確認
1. `F12` でデベロッパーツールを開く
2. "Console" タブを確認
3. 以下のログメッセージを探す：
   - "Incorrect button clicked with:"
   - "Data received - Query:"
   - "Right-click data from button:"

### 拡張機能ログ確認
1. `chrome://extensions/` で拡張機能の詳細を開く
2. "Service Worker" の "検査" をクリック
3. コンソールでエラーやログを確認

## 修正された機能

- ✅ data属性を使用した確実なデータ受け渡し
- ✅ イベントデリゲーションによる動的ボタン対応
- ✅ 複数のイベントハンドリング方法（ID とクラス）
- ✅ content.js での追加のイベントキャプチャー
- ✅ ポップアップと右クリックメニューの両方対応