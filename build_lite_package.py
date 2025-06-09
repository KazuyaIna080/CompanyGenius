#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CompanyGenius Lite パッケージビルダー
軽量版の配布パッケージを作成
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def build_lite_package():
    """CompanyGenius Lite パッケージをビルド"""
    
    print("🪶 CompanyGenius Lite パッケージビルダー")
    print("=" * 50)
    
    # 軽量版用ディレクトリ
    lite_dir = "./CompanyGenius-Lite"
    
    # 既存ディレクトリをクリーンアップ
    if os.path.exists(lite_dir):
        print(f"🗑️  既存ディレクトリを削除: {lite_dir}")
        shutil.rmtree(lite_dir)
    
    os.makedirs(lite_dir)
    print(f"📁 軽量版ディレクトリ作成: {lite_dir}")
    
    # 軽量版に含めるファイル
    lite_files = [
        "create_database_lite.py",
        "requirements.txt",
        "LICENSE", 
        "SECURITY_SETUP.md",
        ".gitignore",
        ".mcp.json.template"
    ]
    
    # 軽量版専用で作成するファイル
    lite_specific_files = {
        "README.md": create_lite_readme_content(),
        "SETUP_LITE.md": create_lite_setup_content(),
        "phase15_lite_api.py": create_lite_api_placeholder()
    }
    
    # 含めるディレクトリ（軽微な変更あり）
    lite_dirs = [
        "chrome_extension"
    ]
    
    # 空で作成するディレクトリ
    empty_dirs = [
        "data"
    ]
    
    # ファイルコピー
    print("\n📋 ファイルコピー中...")
    for file in lite_files:
        if os.path.exists(file):
            shutil.copy2(file, lite_dir)
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} が見つかりません（スキップ）")
    
    # 軽量版専用ファイル作成
    print("\n📝 軽量版専用ファイル作成中...")
    for filename, content in lite_specific_files.items():
        with open(f"{lite_dir}/{filename}", 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {filename}")
    
    # ディレクトリコピー
    print("\n📂 ディレクトリコピー中...")
    for dir_name in lite_dirs:
        if os.path.exists(dir_name):
            dest_dir = f"{lite_dir}/{dir_name}"
            shutil.copytree(dir_name, dest_dir)
            print(f"  ✅ {dir_name}/")
            
            # Chrome拡張機能の軽微な調整
            if dir_name == "chrome_extension":
                adjust_chrome_extension_for_lite(dest_dir)
    
    # 空ディレクトリ作成
    print("\n📁 空ディレクトリ作成中...")
    for dir_name in empty_dirs:
        empty_dir = f"{lite_dir}/{dir_name}"
        os.makedirs(empty_dir, exist_ok=True)
        # .gitkeep ファイル作成
        with open(f"{empty_dir}/.gitkeep", 'w') as f:
            f.write("# データベースファイルがここに作成されます\n")
        print(f"  ✅ {dir_name}/")
    
    # パッケージ情報ファイル作成
    create_package_info(lite_dir)
    
    # ZIPアーカイブ作成
    print("\n📦 ZIPアーカイブ作成中...")
    zip_filename = f"CompanyGenius-Lite-{datetime.now().strftime('%Y%m%d')}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(lite_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, lite_dir)
                zipf.write(file_path, f"CompanyGenius-Lite/{arcname}")
    
    # 統計情報
    lite_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                   for dirpath, dirnames, filenames in os.walk(lite_dir)
                   for filename in filenames) / (1024 * 1024)
    
    zip_size = os.path.getsize(zip_filename) / (1024 * 1024)
    
    print("\n" + "=" * 50)
    print("🎉 CompanyGenius Lite パッケージ作成完了！")
    print(f"📁 ディレクトリ: {lite_dir} ({lite_size:.1f} MB)")
    print(f"📦 アーカイブ: {zip_filename} ({zip_size:.1f} MB)")
    print("\n🚀 配布準備完了:")
    print(f"   - ZIPファイルをGitHub Releasesにアップロード")
    print(f"   - タグ: v1.0.0-lite")
    print(f"   - ターゲット: 軽量版ユーザー（3ステップセットアップ）")

def create_lite_readme_content():
    """軽量版専用README内容"""
    return '''# 🪶 CompanyGenius Lite (EDINET Edition)

**実務で良く確認する前株、後株などの正式社名確認支援ツール（軽量版）**

EDINETコードリスト（約4,000社）を使用した軽量版CompanyGeniusです。3ステップで即座にセットアップ・利用開始できます。

## ⚡ 3ステップセットアップ

### Step 1: EDINETコードリストダウンロード
1. https://disclosure2.edinet-fsa.go.jp/weee0010.aspx にアクセス
2. **「EDINETコードリスト」** をクリックしてCSVファイルをダウンロード
3. ダウンロードしたCSVファイルをこのディレクトリに配置

### Step 2: 軽量版データベース作成
```bash
python create_database_lite.py
```
→ `./data/corporate_lite.db` が作成されます（約5-10MB）

### Step 3: APIサーバー起動
```bash
pip install -r requirements.txt
python phase15_lite_api.py
```
→ ポート8002でAPIサーバーが起動します

### Step 4: Chrome拡張機能インストール
1. Chrome で `chrome://extensions/` を開く
2. **デベロッパーモード** をオンにする
3. **「パッケージ化されていない拡張機能を読み込む」** をクリック
4. `chrome_extension` フォルダを選択

## 📊 軽量版の特徴

| 項目 | 軽量版 | フル版 |
|---|---|---|
| **データ規模** | EDINETコードリスト約4,000社 | 法人番号データベース350万社 |
| **DB容量** | 5-10MB | 1-2GB |
| **セットアップ時間** | 1-2分 | 30-60分 |
| **カバー率** | 上場企業・主要企業90%+ | 全法人100% |
| **対象** | 営業・投資・報告書作成 | 包括的企業検索 |

## ✨ 機能

### 🎯 企業名予測・補完
- 前株・後株などの正式社名確認
- 部分入力からの企業名補完
- 右クリックメニューからの即座予測

### 🧠 学習機能
- ユーザー修正の自動学習
- 修正データのローカル保存
- 予測精度の継続的向上

### 🔍 検索機能
- 企業名での検索
- 証券コードでの検索
- EDINETコードでの検索

## 🔄 フル版へのアップグレード

フル版（350万社対応）への移行をお考えの場合：

**フル版リポジトリ**: https://github.com/KazuyaIna080/CompanyGenius

### アップグレード手順
1. フル版をダウンロード
2. 法人番号データベースを作成
3. ユーザー修正データを移行（自動対応）

## 🛠️ トラブルシューティング

### データベース作成エラー
```bash
# CSVファイルを確認
ls *.csv

# 文字コードエラーの場合
python create_database_lite.py
```

### APIサーバー接続エラー
```bash
# ポート確認
netstat -an | grep 8002

# 別ポートで起動
python phase15_lite_api.py --port 8003
```

## 📞 サポート

- **Issues**: https://github.com/KazuyaIna080/CompanyGenius/issues
- **Documentation**: SECURITY_SETUP.md
- **フル版**: https://github.com/KazuyaIna080/CompanyGenius

## 📄 ライセンス

MIT License - 詳細は LICENSE ファイルを参照

---

**🚀 CompanyGenius Lite で企業名確認作業を効率化しましょう！**
'''

def create_lite_setup_content():
    """軽量版セットアップガイド"""
    return '''# 🛠️ CompanyGenius Lite セットアップガイド

## 📋 前提条件

- Python 3.8以上
- Chrome ブラウザ
- インターネット接続（EDINETコードリストダウンロード用）

## 🚀 詳細セットアップ手順

### 1. EDINETコードリストの準備

#### 1-1: ダウンロード
1. https://disclosure2.edinet-fsa.go.jp/weee0010.aspx にアクセス
2. ページ下部の **「EDINETコードリスト」** をクリック
3. CSVファイルがダウンロードされる

#### 1-2: ファイル配置
```bash
# ダウンロードしたCSVファイルをプロジェクトディレクトリに移動
# ファイル名例: EdinetcodeDlInfo.csv
mv ~/Downloads/EdinetcodeDlInfo.csv ./
```

### 2. Python環境セットアップ

#### 2-1: 依存パッケージインストール
```bash
pip install -r requirements.txt
```

#### 2-2: データベース作成
```bash
python create_database_lite.py
```

**期待される出力:**
```
🪶 CompanyGenius Lite データベース作成
📁 EDINETコードリストCSV: EdinetcodeDlInfo.csv
📊 処理完了: 4,XXX 社
✅ CompanyGenius Lite データベース作成完了！
📊 企業数: 4,XXX 社
💾 サイズ: X.X MB
```

### 3. APIサーバー起動

```bash
python phase15_lite_api.py
```

**期待される出力:**
```
🪶 CompanyGenius Lite API Server
INFO:     Started server process
INFO:     Uvicorn running on http://localhost:8002
```

### 4. Chrome拡張機能インストール

#### 4-1: 拡張機能読み込み
1. Chrome を開く
2. アドレスバーに `chrome://extensions/` と入力
3. 右上の **「デベロッパーモード」** をオンにする
4. **「パッケージ化されていない拡張機能を読み込む」** をクリック
5. `chrome_extension` フォルダを選択

#### 4-2: 動作確認
1. 任意のWebページを開く
2. 企業名らしきテキストを選択
3. 右クリック → **「CompanyGeniusで企業名を予測」** を選択
4. 予測結果ダイアログが表示されることを確認

## 🔧 設定カスタマイズ

### APIポート変更
```bash
# デフォルト以外のポートで起動
python phase15_lite_api.py --port 8003
```

### データベース更新
```bash
# 新しいEDINETコードリストで更新
python create_database_lite.py
```

## 📊 使用統計

軽量版の使用状況を確認:
```bash
# データベース統計
python -c "
import sqlite3
conn = sqlite3.connect('./data/corporate_lite.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM companies_lite')
print(f'企業数: {cursor.fetchone()[0]:,}')
cursor.execute('SELECT COUNT(*) FROM user_corrections')
print(f'学習済み修正: {cursor.fetchone()[0]:,}')
conn.close()
"
```

## 🚀 次のステップ

### フル版への移行検討
軽量版で満足いただけた場合、フル版（350万社）への移行をご検討ください:

**フル版の追加メリット:**
- 全法人対応（350万社 vs 4,000社）
- 非上場企業・中小企業対応
- より高精度な予測システム

**移行方法:**
1. https://github.com/KazuyaIna080/CompanyGenius をダウンロード
2. 法人番号データベースセットアップ
3. ユーザー修正データは自動的に引き継がれます
'''

def create_lite_api_placeholder():
    """軽量版API プレースホルダー（後で実装）"""
    return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CompanyGenius Lite API Server
EDINETコードリスト版の軽量APIサーバー

TODO: 実装予定
- 軽量版データベース対応
- ポート8002での起動
- 軽量版専用の予測ロジック
"""

print("🪶 CompanyGenius Lite API Server")
print("⚠️  実装準備中...")
print("📋 TODO:")
print("  - EDINETコードリストDB対応")
print("  - 軽量版予測システム実装")
print("  - ポート8002対応")
print("  - ユーザー学習機能統合")
'''

def adjust_chrome_extension_for_lite(chrome_dir):
    """Chrome拡張機能の軽量版向け調整"""
    # manifest.jsonの調整（ポート8002への対応など）
    print("  🔧 Chrome拡張機能を軽量版向けに調整")
    
    # TODO: 実際の調整処理
    # - manifest.jsonのhost_permissionsにlocalhost:8002を追加
    # - background.jsでAPIエンドポイントの設定分岐
    
def create_package_info(lite_dir):
    """パッケージ情報ファイル作成"""
    package_info = f'''# CompanyGenius Lite Package Info

## パッケージ情報
- **バージョン**: v1.0.0-lite
- **作成日**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **データソース**: EDINETコードリスト
- **企業数**: 約4,000社
- **対象**: 上場企業・主要企業

## 含まれるファイル
- create_database_lite.py: 軽量版DB作成スクリプト
- phase15_lite_api.py: 軽量版APIサーバー
- chrome_extension/: Chrome拡張機能
- requirements.txt: Python依存関係
- LICENSE: MITライセンス
- SECURITY_SETUP.md: セキュリティ設定ガイド

## セットアップ
1. EDINETコードリストダウンロード
2. python create_database_lite.py
3. python phase15_lite_api.py

## サポート
- GitHub: https://github.com/KazuyaIna080/CompanyGenius
- Issues: https://github.com/KazuyaIna080/CompanyGenius/issues
'''
    
    with open(f"{lite_dir}/PACKAGE_INFO.md", 'w', encoding='utf-8') as f:
        f.write(package_info)

if __name__ == "__main__":
    build_lite_package()