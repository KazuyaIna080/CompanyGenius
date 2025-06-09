# 🎯 シンプルGitHubアップロード方法

## 方法1: GitHub Web UI で直接アップロード（最も簡単）

### Step 1: ZIPファイル作成
```bash
# 現在のディレクトリで実行
zip -r CompanyGenius.zip . -x "*.log" "corrections.log" "server.log" ".git/*"
```

### Step 2: GitHub Web UI でアップロード
1. https://github.com/KazuyaIna080/CompanyGenius にアクセス
2. **「uploading an existing file」** をクリック
3. CompanyGenius.zip をドラッグ&ドロップ
4. Commit message: `🧠 CompanyGenius v1.0.0 - Initial release`
5. **「Commit changes」** をクリック

### Step 3: ZIPを展開（GitHub上で）
GitHubが自動的にZIPを展開してくれます。

---

## 方法2: GitHub Desktop使用（GUI）

### Step 1: GitHub Desktop ダウンロード
- https://desktop.github.com/
- インストール後、GitHubアカウントでログイン

### Step 2: ローカルリポジトリを追加
1. **File → Add Local Repository**
2. `/home/kazin/claude_code` を選択
3. **Publish repository** をクリック

---

## 方法3: コマンドライン認証修正

### 問題の原因
- Personal Access Token が必要
- または SSH キー設定が必要

### 簡単修正方法
```bash
# 1. 既存のremoteを削除
git remote remove origin

# 2. SSH URLで再設定（推奨）
git remote add origin git@github.com:KazuyaIna080/CompanyGenius.git

# 3. SSH キー確認
ls ~/.ssh/
```

### SSH キーが無い場合
```bash
# SSH キー生成
ssh-keygen -t ed25519 -C "kazuya.inagaki080@gmail.com"
# Enter連打でOK

# 公開キーをコピー
cat ~/.ssh/id_ed25519.pub
```

GitHubのSettings → SSH and GPG keys → New SSH key に貼り付け

---

## 推奨: 方法1（Web UI）が最も確実

ZIP作成から始めましょうか？