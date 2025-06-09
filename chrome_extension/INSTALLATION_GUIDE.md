# 🚀 CompanyGenius インストールガイド

## 📋 必要な環境

### システム要件
- **Chrome Browser**: Version 88+ (Manifest V3対応)
- **Python**: 3.7+ (APIサーバー用)
- **OS**: Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+
- **メモリ**: 最低2GB RAM
- **ディスク**: 100MB以上の空き容量

### 開発環境 (開発者向け)
- **Git**: バージョン管理
- **Code Editor**: VS Code推奨
- **Terminal**: コマンドライン操作

---

## 🛠️ インストール手順

### Step 1: ファイルの準備

#### Git使用の場合
```bash
git clone <repository-url>
cd CompanyGenius
```

#### ZIPダウンロードの場合
1. プロジェクトファイルをダウンロード
2. 適当なフォルダに解凍
3. コマンドプロンプト/ターミナルで解凍先に移動

### Step 2: APIサーバーの起動

#### Windows (PowerShell)
```powershell
# プロジェクトディレクトリに移動
cd path\to\CompanyGenius

# APIサーバー起動
python phase15_fixed_api.py
```

#### macOS/Linux (Terminal)
```bash
# プロジェクトディレクトリに移動
cd /path/to/CompanyGenius

# APIサーバー起動
python3 phase15_fixed_api.py
```

**✅ 成功メッセージ例:**
```
🌟 Phase 15: UTF-8 Fixed API Server Starting
✅ Fixed server running on http://0.0.0.0:8001
🎯 文字化け0%品質基準達成版
Press Ctrl+C to stop the server
```

### Step 3: Chrome拡張機能のインストール

1. **Chrome拡張機能ページを開く**
   - アドレスバーに `chrome://extensions/` と入力してEnter

2. **開発者モードを有効化**
   - 右上の「開発者モード」トグルをONにする

3. **拡張機能を読み込み**
   - 「パッケージ化されていない拡張機能を読み込む」をクリック
   - `chrome_extension` フォルダを選択
   - 「フォルダーの選択」をクリック

4. **インストール確認**
   - CompanyGeniusアイコンがツールバーに表示される
   - 拡張機能一覧に「CompanyGenius」が表示される

### Step 4: 動作確認

#### 基本機能テスト
1. **ポップアップテスト**
   - ツールバーのCompanyGeniusアイコンをクリック
   - 「トヨタ」と入力して「予測実行」をクリック
   - 予測結果が表示されることを確認

2. **右クリックメニューテスト**
   - 任意のWebページで「ソニー」などのテキストを選択
   - 右クリックして「CompanyGenius で企業名を予測」を選択
   - 予測ダイアログが表示されることを確認

#### 学習機能テスト
1. 予測結果の「❌ 間違い」ボタンをクリック
2. 正しい企業名を入力して「✅ 修正を送信」
3. 同じ企業名で再度予測して学習結果が反映されることを確認

---

## 🔧 トラブルシューティング

### 🚨 よくある問題と解決方法

#### 1. APIサーバーが起動しない

**症状**: `python phase15_fixed_api.py` でエラー
```
ModuleNotFoundError: No module named 'phase15_final_system'
```

**解決方法**:
```bash
# 正しいディレクトリにいることを確認
pwd  # または dir (Windows)
ls   # または dir (Windows) でファイル一覧確認

# phase15_final_system.pyが存在することを確認
ls phase15_final_system.py
```

#### 2. 拡張機能が表示されない

**症状**: Chrome拡張機能一覧にCompanyGeniusが表示されない

**解決方法**:
1. **開発者モードの確認**: `chrome://extensions/` で開発者モードがONか確認
2. **フォルダ選択の確認**: `chrome_extension` フォルダ自体を選択
3. **manifest.jsonの確認**: フォルダ内に `manifest.json` があることを確認

#### 3. 予測機能が動作しない

**症状**: 右クリックメニューが表示されない、または予測エラー

**解決方法**:
```bash
# APIサーバーの動作確認
curl http://localhost:8001/health

# または Webブラウザで以下URLにアクセス
# http://localhost:8001/health
```

**期待される応答**:
```json
{
  "status": "healthy",
  "accuracy": "100%",
  "system": "Phase 15 Final - Character Code Fixed"
}
```

#### 4. 文字化けが発生する

**症状**: 予測結果が「ãã³ã¢ã»ãã¯ãã­ã¸」のように表示される

**解決方法**:
```bash
# Windows: UTF-8エンコーディング設定
chcp 65001

# macOS/Linux: ロケール確認
locale
export LANG=ja_JP.UTF-8
```

#### 5. 学習機能が働かない

**症状**: 修正を送信しても次回予測で反映されない

**解決方法**:
1. **ログファイル確認**: `corrections.log` に修正データが保存されているか確認
2. **APIサーバー再起動**: Ctrl+C で停止後、再度 `python3 phase15_fixed_api.py`
3. **拡張機能再読み込み**: `chrome://extensions/` で「再読み込み」ボタンをクリック

---

## 🔍 デバッグ方法

### ログの確認

#### サーバーログ
```bash
# リアルタイム監視
tail -f server.log

# 最新50行表示
tail -50 server.log
```

#### Chrome拡張機能ログ
1. `chrome://extensions/` を開く
2. CompanyGeniusの「詳細」をクリック
3. 「Service Worker」の「検査」をクリック
4. Consoleタブでログ確認

#### 学習データ確認
```bash
# 修正データの確認
cat corrections.log

# または最新5件のみ
tail -5 corrections.log
```

### API動作確認

#### 直接APIテスト
```bash
# 健康状態チェック
curl http://localhost:8001/health

# 予測テスト
curl "http://localhost:8001/predict?q=トヨタ"

# 文字コードテスト
curl http://localhost:8001/charset_test
```

---

## 📊 正常動作の確認項目

### ✅ チェックリスト

- [ ] **APIサーバー起動**: `http://localhost:8001/health` でレスポンス取得
- [ ] **拡張機能表示**: Chrome拡張機能一覧でCompanyGenius確認
- [ ] **ポップアップ動作**: アイコンクリックでポップアップ表示
- [ ] **右クリックメニュー**: テキスト選択時にメニュー表示
- [ ] **予測機能**: 企業名予測が正常動作
- [ ] **修正機能**: 「❌ 間違い」ボタンが動作
- [ ] **学習機能**: 修正後の予測で改善結果が反映
- [ ] **文字コード**: 日本語が正しく表示される

### 🎯 パフォーマンス確認

- **予測速度**: <100ms での応答
- **文字化け**: 0% (完全なUTF-8処理)
- **学習反映**: 修正後即座に100%精度で予測
- **メモリ使用量**: <50MB の拡張機能メモリ使用

---

## 🚀 高度な設定

### カスタマイズオプション

#### APIポート変更
```python
# phase15_fixed_api.py の560行目
PORT = 8001  # お好みのポートに変更

# manifest.json も対応するポートに変更
"host_permissions": [
    "http://localhost:8001/*"  # 新しいポートに更新
]
```

#### 学習データのバックアップ
```bash
# 学習データをバックアップ
cp corrections.log corrections_backup_$(date +%Y%m%d).log

# 学習データのリセット
rm corrections.log
```

#### ログレベル調整
```python
# より詳細なログを出力したい場合
# phase15_final_system.py でprint文を追加
print(f"🔍 Detailed debug: {variable_name}")
```

---

## 📞 サポート

### 問題が解決しない場合

1. **ログファイルの確認**: `server.log` と `corrections.log` の内容
2. **環境情報の確認**: OS、Chrome バージョン、Python バージョン
3. **エラーメッセージ**: 完全なエラーメッセージをコピー
4. **再現手順**: 問題が発生する具体的な操作手順

### 問い合わせ前のチェック

- [ ] APIサーバーが起動していることを確認
- [ ] Chrome拡張機能が有効になっていることを確認
- [ ] 必要な権限が付与されていることを確認
- [ ] ログファイルでエラーメッセージを確認

---

**🧠 CompanyGenius のインストールが完了しました！**  
**素晴らしいAI予測体験をお楽しみください！** 🎉