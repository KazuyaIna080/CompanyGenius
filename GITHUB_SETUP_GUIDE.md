# 🚀 GitHub初回アップロード完全ガイド

## 📋 事前準備チェックリスト

### ✅ 必要なもの
- [ ] GitHubアカウント（https://github.com）
- [ ] メールアドレス（確認済み）
- [ ] Git がインストール済み（確認方法：`git --version`）
- [ ] CompanyGeniusプロジェクトファイル

---

## 🔧 Step 1: Git初期設定（初回のみ）

### 1-1: Git設定確認
```bash
# 現在の設定確認
git config --global user.name
git config --global user.email
```

### 1-2: Git設定（未設定の場合）
```bash
# あなたの名前とメールアドレスに置き換え
git config --global user.name "あなたの名前"
git config --global user.email "your.email@example.com"

# 設定確認
git config --list
```

**💡 重要**: GitHubに登録したメールアドレスと同じものを使用してください

---

## 🌐 Step 2: GitHubでリポジトリ作成

### 2-1: GitHubにログイン
1. https://github.com にアクセス
2. ユーザー名・パスワードでログイン

### 2-2: 新しいリポジトリ作成
1. **右上の「+」ボタン** → **「New repository」** をクリック

2. **リポジトリ設定**:
   ```
   Repository name: CompanyGenius
   Description: 🧠 AI-powered company name prediction with smart learning
   
   ☑️ Public (誰でも見れる - 推奨)
   ☐ Add a README file (後で追加するのでチェックしない)
   ☐ Add .gitignore (既に作成済み)
   ☐ Choose a license (既に作成済み)
   ```

3. **「Create repository」ボタン** をクリック

### 2-3: リポジトリURLをコピー
作成後の画面で **HTTPS URL** をコピー（例：`https://github.com/あなたのユーザー名/CompanyGenius.git`）

---

## 💻 Step 3: ローカルでGit初期化

### 3-1: プロジェクトディレクトリに移動
```bash
# CompanyGeniusのディレクトリに移動
cd /home/kazin/claude_code
```

### 3-2: Git初期化とファイル追加
```bash
# 1. Gitリポジトリ初期化
git init

# 2. ファイルをステージング（追加準備）
git add .

# 3. 初回コミット作成
git commit -m "🧠 CompanyGenius v1.0.0 - AI-powered company name prediction with smart learning

✨ Features:
- Chrome Extension with popup and right-click context menu
- AI-powered company name prediction
- Smart learning system that improves with user corrections
- Real-time learning with 100% accuracy for corrected names
- Perfect UTF-8 support for Japanese company names
- 7-layer cascade prediction system

🎯 Key Components:
- Chrome Extension (Manifest V3)
- Python API Server with CORS support
- Machine Learning prediction engine
- Learning data persistence system

🚀 Ready for production use!"
```

### 3-3: GitHubリポジトリと接続
```bash
# メインブランチ名を設定
git branch -M main

# GitHubリポジトリをリモートとして追加（URLを自分のものに変更）
git remote add origin https://github.com/あなたのユーザー名/CompanyGenius.git

# GitHubにプッシュ（アップロード）
git push -u origin main
```

---

## 🔐 Step 4: 認証設定（初回のみ）

### パターンA: HTTPS認証（推奨・簡単）

#### 4-1: Personal Access Tokenの作成
1. GitHub → **右上のプロフィール画像** → **Settings**
2. 左メニュー最下部 → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)**

#### 4-2: トークン設定
```
Note: CompanyGenius Project Access
Expiration: 90 days (お好みで調整)

スコープ選択:
☑️ repo (全てのリポジトリアクセス)
☑️ workflow (GitHub Actions)
☑️ write:packages (パッケージ書き込み)
```

5. **Generate token** をクリック
6. **生成されたトークンをコピー**（⚠️ 一度しか表示されません！）

#### 4-3: トークンでプッシュ
```bash
# プッシュ時にパスワードの代わりにトークンを入力
git push -u origin main

# Username: あなたのGitHubユーザー名
# Password: 先ほどコピーしたトークン（パスワードではなく）
```

### パターンB: SSH認証（上級者向け）

#### 4-1: SSH キー生成
```bash
# SSH キーペア生成
ssh-keygen -t ed25519 -C "your.email@example.com"

# Enter file: そのままEnter
# Enter passphrase: お好みで設定（空でもOK）
```

#### 4-2: SSH キーをGitHubに追加
```bash
# 公開キーの内容をコピー
cat ~/.ssh/id_ed25519.pub
```

1. GitHub → **Settings** → **SSH and GPG keys**
2. **New SSH key** をクリック
3. **Title**: "CompanyGenius Development"
4. **Key**: コピーした公開キーを貼り付け
5. **Add SSH key** をクリック

#### 4-3: SSH URLでリモート設定
```bash
# HTTPS URLをSSH URLに変更
git remote set-url origin git@github.com:あなたのユーザー名/CompanyGenius.git

# プッシュ
git push -u origin main
```

---

## ✅ Step 5: アップロード確認

### 5-1: GitHub上での確認
1. ブラウザでリポジトリページを開く
2. 以下のファイル・フォルダが表示されていることを確認：
   ```
   ├── chrome_extension/
   ├── phase15_*.py
   ├── LICENSE
   ├── .gitignore
   ├── README.md
   ├── INSTALLATION_GUIDE.md
   └── その他ドキュメント
   ```

### 5-2: README表示確認
- プロジェクトの説明が美しく表示されているか確認
- 画像やコードブロックが正しく表示されているか確認

---

## 🚀 Step 6: プロジェクトページ最適化

### 6-1: About設定
1. リポジトリページ右上の **⚙️（設定アイコン）** をクリック
2. **Description**: `🧠 AI-powered company name prediction with smart learning`
3. **Website**: （お持ちの場合）
4. **Topics**: `chrome-extension`, `ai`, `machine-learning`, `javascript`, `python`, `productivity`
5. **Save changes**

### 6-2: README.mdの確認・調整
```bash
# READMEに問題があれば修正
nano chrome_extension/README.md

# 修正をコミット・プッシュ
git add chrome_extension/README.md
git commit -m "📝 Update README for better GitHub presentation"
git push
```

---

## 🎯 Step 7: 初回告知・共有

### 7-1: SNS投稿
**Twitter:**
```
🧠 CompanyGenius をオープンソースで公開しました！

AI搭載Chrome拡張機能
✅ 企業名の瞬間予測
✅ 学習機能で精度向上
✅ 日本企業名特化

GitHub: https://github.com/あなたのユーザー名/CompanyGenius

#ChromeExtension #AI #OpenSource #productivity #JavaScript #Python
```

**LinkedIn:**
```
🚀 オープンソースプロジェクト「CompanyGenius」を公開

企業名予測のためのAI搭載Chrome拡張機能を開発・公開しました。

【技術仕様】
• Chrome Extension (Manifest V3)
• Python API Server with Machine Learning
• Real-time Learning System
• Perfect UTF-8 Support

ビジネス効率化にご活用ください。
コントリビューション歓迎！

GitHub: https://github.com/あなたのユーザー名/CompanyGenius

#OpenSource #AI #MachineLearning #ChromeExtension #BusinessEfficiency
```

---

## 🔧 トラブルシューティング

### 問題1: `git: command not found`
**解決方法:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install git

# macOS (Homebrew)
brew install git

# Windows
# Git for Windows をダウンロード・インストール
# https://git-scm.com/download/win
```

### 問題2: `Permission denied (publickey)`
**解決方法:**
1. HTTPS認証に切り替え：
```bash
git remote set-url origin https://github.com/あなたのユーザー名/CompanyGenius.git
```
2. Personal Access Tokenを使用

### 問題3: `fatal: remote origin already exists`
**解決方法:**
```bash
# 既存のリモートを削除して再設定
git remote remove origin
git remote add origin https://github.com/あなたのユーザー名/CompanyGenius.git
```

### 問題4: ファイルサイズが大きすぎる
**解決方法:**
```bash
# 大きなファイルを確認
find . -size +50M -type f

# 不要な大きなファイルを除外
echo "大きなファイル名" >> .gitignore
git rm --cached 大きなファイル名
```

---

## 📊 成功指標

### アップロード後24時間以内
- [ ] GitHubページが正常表示
- [ ] README.mdが美しく表示
- [ ] ライセンス・概要が設定済み
- [ ] 初回SNS投稿完了

### 1週間以内
- [ ] GitHub Stars: 5+
- [ ] Issues/Pull Requests: 初回フィードバック
- [ ] Clone/Download: 10+
- [ ] SNS反応: いいね・リツイート

---

## 🚀 次のステップ

### 継続的改善
```bash
# 日常的な更新フロー
git add .
git commit -m "✨ Add new feature: [機能名]"
git push

# ブランチを使った開発
git checkout -b feature/new-feature
# 開発作業
git add .
git commit -m "🚧 Work in progress: new feature"
git push -u origin feature/new-feature
# GitHub上でPull Request作成
```

### コミュニティ形成
- Issues テンプレート作成
- Contributing ガイドライン作成
- Code of Conduct 追加
- GitHub Actions CI/CD設定

---

**準備ができたら一緒にやってみましょう！** 🎉

どこか分からないところがあったら遠慮なく聞いてください！