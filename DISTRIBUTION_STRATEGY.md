# 📦 CompanyGenius 配布戦略：標準版・軽量版分離

## 🎯 配布戦略の選択肢

### Option A: GitHub Branches（推奨）

**メインブランチ構成:**
```
main (標準版 - フル機能)
├── lite (軽量版専用ブランチ)
└── releases/ (各バージョンタグ)
```

**実装方法:**
```bash
# 軽量版ブランチ作成
git checkout -b lite
git push -u origin lite

# 軽量版専用のファイル構成
CompanyGenius/ (main branch)
├── 標準版ファイル群
└── 軽量版共通ファイル

CompanyGenius/ (lite branch) 
├── 軽量版専用ファイル群
├── README_LITE.md
└── 標準版から軽量版への案内
```

### Option B: GitHub Releases（最も実用的）

**単一リポジトリ + 複数リリース:**
```
リポジトリ: KazuyaIna080/CompanyGenius

Releases:
├── v1.0.0-full (標準版)
│   └── CompanyGenius-Full-v1.0.0.zip
├── v1.0.0-lite (軽量版)  
│   └── CompanyGenius-Lite-v1.0.0.zip
└── v1.0.0 (統合版 - 両方含む)
    └── CompanyGenius-Complete-v1.0.0.zip
```

### Option C: 別リポジトリ

**完全分離:**
```
KazuyaIna080/CompanyGenius (標準版)
KazuyaIna080/CompanyGenius-Lite (軽量版)
```

---

## 🚀 推奨アプローチ：GitHub Releases + タグ戦略

### 現在の実装案

```bash
# 標準版リリース
git tag v1.0.0-full
git push origin v1.0.0-full

# 軽量版用のファイル調整
# 軽量版に不要なファイルを除外したアーカイブ作成
python build_lite_package.py

# 軽量版リリース
git tag v1.0.0-lite  
git push origin v1.0.0-lite

# GitHub Releases で別々にアップロード
gh release create v1.0.0-full \
  --title "CompanyGenius Full v1.0.0" \
  --notes "完全版（350万社、1-2GB）"

gh release create v1.0.0-lite \
  CompanyGenius-Lite.zip \
  --title "CompanyGenius Lite v1.0.0" \
  --notes "軽量版（EDINETコードリスト、5-10MB）"
```

---

## 🔧 軽量版パッケージビルダー

```python
# build_lite_package.py
import os
import shutil
import zipfile
from pathlib import Path

def build_lite_package():
    """CompanyGenius Lite パッケージをビルド"""
    
    # 軽量版用ディレクトリ
    lite_dir = "./CompanyGenius-Lite"
    
    # 既存ディレクトリをクリーンアップ
    if os.path.exists(lite_dir):
        shutil.rmtree(lite_dir)
    
    os.makedirs(lite_dir)
    
    # 軽量版に含めるファイル
    lite_files = [
        "create_database_lite.py",
        "phase15_lite_api.py",  # 作成予定
        "requirements.txt",
        "LICENSE",
        "README_LITE.md",  # 作成予定
        "SETUP_LITE.md",   # 作成予定
        "SECURITY_SETUP.md",
        ".gitignore"
    ]
    
    # ディレクトリ
    lite_dirs = [
        "chrome_extension",  # 設定のみ軽微変更
        "data"  # 空ディレクトリとして作成
    ]
    
    # ファイルコピー
    for file in lite_files:
        if os.path.exists(file):
            shutil.copy2(file, lite_dir)
    
    # ディレクトリコピー
    for dir_name in lite_dirs:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, f"{lite_dir}/{dir_name}")
        else:
            os.makedirs(f"{lite_dir}/{dir_name}")
    
    # 軽量版専用README作成
    create_lite_readme(lite_dir)
    
    # ZIPアーカイブ作成
    with zipfile.ZipFile("CompanyGenius-Lite.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(lite_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, lite_dir)
                zipf.write(file_path, f"CompanyGenius-Lite/{arcname}")
    
    print("✅ CompanyGenius Lite パッケージ作成完了: CompanyGenius-Lite.zip")

def create_lite_readme(lite_dir):
    """軽量版専用README作成"""
    readme_content = '''# 🪶 CompanyGenius Lite (EDINET Edition)

## ⚡ 3ステップセットアップ

### Step 1: EDINETコードリストダウンロード
1. https://disclosure2.edinet-fsa.go.jp/weee0010.aspx にアクセス
2. 「EDINETコードリスト」をダウンロード
3. ダウンロードしたCSVファイルをこのディレクトリに配置

### Step 2: 軽量版データベース作成
```bash
python create_database_lite.py
```

### Step 3: APIサーバー起動
```bash
python phase15_lite_api.py
```

### Step 4: Chrome拡張機能インストール
1. Chrome → chrome://extensions/
2. デベロッパーモード ON
3. chrome_extension フォルダを選択

## 📊 軽量版の特徴

- **データ規模**: EDINETコードリスト約4,000社（5-10MB）
- **セットアップ時間**: 1-2分
- **カバー率**: 上場企業・主要企業90%+
- **機能**: ユーザー学習機能完全対応

## 🔄 フル版へのアップグレード

フル版（350万社対応）はメインリポジトリから：
https://github.com/KazuyaIna080/CompanyGenius

## 📞 サポート

- Issues: https://github.com/KazuyaIna080/CompanyGenius/issues
- Documentation: README.md, SECURITY_SETUP.md
'''
    
    with open(f"{lite_dir}/README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == "__main__":
    build_lite_package()
```

---

## 📋 実装手順

### Phase 1: 軽量版API作成

```python
# phase15_lite_api.py（作成予定）
# 軽量版専用のAPIサーバー
# - corporate_lite.db を使用
# - ポート8002で起動
# - 軽量版専用の予測ロジック
```

### Phase 2: Chrome拡張機能の設定分岐

```javascript
// chrome_extension/background.js に設定分岐追加
const API_ENDPOINTS = {
    full: 'http://localhost:8001',
    lite: 'http://localhost:8002'
};

// 設定により切り替え
const API_URL = localStorage.getItem('companygenius_mode') === 'lite' 
    ? API_ENDPOINTS.lite 
    : API_ENDPOINTS.full;
```

### Phase 3: リリース作成

```bash
# ビルド実行
python build_lite_package.py

# リリース作成
gh release create v1.0.0-lite \
  CompanyGenius-Lite.zip \
  --title "🪶 CompanyGenius Lite v1.0.0" \
  --notes "軽量版（EDINETコードリスト、3ステップセットアップ）"

gh release create v1.0.0-full \
  --title "🏢 CompanyGenius Full v1.0.0" \
  --notes "完全版（350万社、法人番号データベース）"
```

---

## 🎯 ユーザー体験

### 軽量版ユーザー
1. GitHub → Releases → v1.0.0-lite
2. CompanyGenius-Lite.zip ダウンロード
3. 3ステップセットアップで即座利用開始

### 標準版ユーザー  
1. GitHub → メインページまたはv1.0.0-full
2. 詳細セットアップガイドに従って構築
3. 大容量データベースでフル機能利用

### アップグレードパス
- 軽量版で試用 → 満足 → 標準版に移行
- ユーザー修正データは両方で共有可能

---

## 📊 配布統計・効果測定

### 想定ダウンロード比率
- **軽量版**: 80%（導入簡単、お試し用途）
- **標準版**: 20%（本格運用、完全機能必要）

### 成功指標
- 軽量版ダウンロード数
- 軽量版→標準版コンバージョン率
- ユーザーフィードバック・満足度
- 実際の使用継続率

**最適解：GitHub Releases + タグ戦略で、両方を効率的に配布・管理**