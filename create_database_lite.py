#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CompanyGenius Lite データベース作成スクリプト
EDINETコードリストCSVからSQLiteデータベースを作成

データソース: https://disclosure2.edinet-fsa.go.jp/weee0010.aspx
ファイル: EDINETコードリスト（CSVファイル）
"""

import csv
import sqlite3
import os
import glob
import sys
from datetime import datetime

class CompanyGeniusLiteBuilder:
    """CompanyGenius Lite データベース作成（EDINETコードリスト版）"""
    
    def __init__(self):
        self.db_path = "./data/corporate_lite.db"
        self.csv_file = None
        self.companies = []
    
    def find_edinet_csv(self):
        """EDINETコードリストCSVファイルを検索"""
        print("🔍 EDINETコードリストCSVファイルを検索中...")
        
        # 一般的なファイル名パターン
        patterns = [
            "EdinetcodeDlInfo.csv",
            "edinet_code_list.csv", 
            "edinetcode*.csv",
            "*edinet*.csv",
            "*EDINET*.csv"
        ]
        
        for pattern in patterns:
            files = glob.glob(pattern)
            if files:
                self.csv_file = files[0]
                print(f"✅ EDINETコードリストCSV: {self.csv_file}")
                return True
        
        print("❌ EDINETコードリストCSVが見つかりません")
        print()
        print("📥 EDINETコードリストのダウンロード手順:")
        print("1. https://disclosure2.edinet-fsa.go.jp/weee0010.aspx にアクセス")
        print("2. 「EDINETコードリスト」をクリックしてダウンロード")
        print("3. ダウンロードしたCSVファイルをこのディレクトリに配置")
        print("4. 再度このスクリプトを実行")
        print()
        return False
    
    def process_edinet_csv(self):
        """EDINETコードリストCSVを処理"""
        if not self.csv_file:
            return False
        
        print("📊 EDINETコードリスト処理中...")
        
        try:
            # 文字コード自動検出（EDINETはShift_JIS/CP932の場合が多い）
            encodings = ['cp932', 'shift_jis', 'utf-8', 'utf-8-sig']
            
            for encoding in encodings:
                try:
                    with open(self.csv_file, 'r', encoding=encoding) as f:
                        # ヘッダー行を確認
                        first_line = f.readline()
                        if 'EDINET' in first_line or 'edinet' in first_line or 'コード' in first_line:
                            print(f"📝 文字コード: {encoding}")
                            break
                except UnicodeDecodeError:
                    continue
            else:
                print("❌ CSVファイルの文字コードを特定できません")
                return False
            
            # CSVファイル読み込み
            with open(self.csv_file, 'r', encoding=encoding) as f:
                # BOM除去
                content = f.read()
                if content.startswith('\ufeff'):
                    content = content[1:]
                
                lines = content.splitlines()
                reader = csv.DictReader(lines)
                
                company_count = 0
                for row in reader:
                    # EDINETコードリストの標準フィールド（日本語と英語）
                    # フィールド名の正規化（様々な形式に対応）
                    edinet_code = (row.get('ＥＤＩＮＥＴコード') or 
                                  row.get('EDINETコード') or 
                                  row.get('EDINET_CODE') or 
                                  row.get('edinetCode', '')).strip()
                    
                    submitter_name = (row.get('提出者名') or 
                                    row.get('SUBMITTER_NAME') or 
                                    row.get('submitterName', '')).strip()
                    
                    securities_code = (row.get('証券コード') or 
                                     row.get('SECURITIES_CODE') or 
                                     row.get('securitiesCode', '')).strip()
                    
                    # 有効な企業データのみ追加
                    if submitter_name and edinet_code:
                        company_info = {
                            'edinet_code': edinet_code,
                            'submitter_name': submitter_name,
                            'submitter_name_en': (row.get('提出者名（英字）') or 
                                                 row.get('SUBMITTER_NAME_EN') or 
                                                 row.get('submitterNameEn', '')).strip(),
                            'submitter_name_kana': (row.get('提出者名（ヨミ）') or 
                                                   row.get('SUBMITTER_NAME_KANA') or 
                                                   row.get('submitterNameKana', '')).strip(),
                            'securities_code': securities_code,
                            'corporate_number': (row.get('提出者法人番号') or 
                                               row.get('SUBMITTER_CORPORATE_NUMBER') or 
                                               row.get('submitterCorporateNumber', '')).strip(),
                            'listing_classification': (row.get('上場区分') or 
                                                     row.get('LISTING_CLASSIFICATION') or 
                                                     row.get('listingClassification', '')).strip(),
                            'industry': (row.get('提出者業種') or 
                                       row.get('SUBMITTER_INDUSTRY') or 
                                       row.get('submitterIndustry', '')).strip(),
                            'location': (row.get('所在地') or 
                                       row.get('LOCATION') or 
                                       row.get('location', '')).strip()
                        }
                        
                        self.companies.append(company_info)
                        company_count += 1
                
                print(f"✅ 処理完了: {company_count} 社")
                return True
                
        except Exception as e:
            print(f"❌ CSVファイル処理エラー: {str(e)}")
            return False
    
    def create_lite_database(self):
        """CompanyGenius Lite データベース作成"""
        print("🏗️  CompanyGenius Lite データベース作成中...")
        
        # データディレクトリ作成
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # 既存データベースの確認
        if os.path.exists(self.db_path):
            response = input(f"⚠️  既存のLiteデータベースが見つかりました: {self.db_path}\n上書きしますか？ (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("❌ 処理を中止しました")
                return False
            os.remove(self.db_path)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # CompanyGenius Lite テーブル作成
        cursor.execute('''
            CREATE TABLE companies_lite (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                edinet_code TEXT UNIQUE,
                company_name TEXT,
                company_name_en TEXT,
                company_name_kana TEXT,
                securities_code TEXT,
                corporate_number TEXT,
                listing_classification TEXT,
                industry TEXT,
                location TEXT,
                last_updated TEXT
            )
        ''')
        
        # ユーザー修正データテーブル（フル版と共通構造）
        cursor.execute('''
            CREATE TABLE user_corrections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_query TEXT,
                predicted_name TEXT,
                correct_name TEXT,
                correction_date TEXT,
                confidence REAL DEFAULT 1.0
            )
        ''')
        
        # データ挿入
        for company in self.companies:
            cursor.execute('''
                INSERT OR REPLACE INTO companies_lite VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                None,
                company['edinet_code'],
                company['submitter_name'],
                company['submitter_name_en'],
                company['submitter_name_kana'],
                company['securities_code'],
                company['corporate_number'],
                company['listing_classification'],
                company['industry'],
                company['location'],
                datetime.now().isoformat()
            ))
        
        # 検索用インデックス
        print("🔍 検索インデックス作成中...")
        cursor.execute('CREATE INDEX idx_lite_name ON companies_lite(company_name)')
        cursor.execute('CREATE INDEX idx_lite_kana ON companies_lite(company_name_kana)')
        cursor.execute('CREATE INDEX idx_lite_securities ON companies_lite(securities_code)')
        cursor.execute('CREATE INDEX idx_lite_edinet ON companies_lite(edinet_code)')
        
        # ユーザー修正データ用インデックス
        cursor.execute('CREATE INDEX idx_corrections_query ON user_corrections(original_query)')
        
        conn.commit()
        conn.close()
        
        # 統計情報
        db_size = os.path.getsize(self.db_path) / (1024 * 1024)  # MB
        
        print("\n" + "=" * 50)
        print("🎉 CompanyGenius Lite データベース作成完了！")
        print(f"📁 ファイル: {self.db_path}")
        print(f"📊 企業数: {len(self.companies)} 社")
        print(f"💾 サイズ: {db_size:.1f} MB")
        print(f"⏱️  セットアップ時間: 1-2分")
        print("\n🚀 Lite版APIサーバーを起動できます:")
        print("   python phase15_lite_api.py")
        print("\n📱 Chrome拡張機能:")
        print("   既存のchrome_extensionフォルダをChromeにインストール")
        print("   （APIサーバーが自動的にLite版DBを使用）")
        
        return True

def main():
    """CompanyGenius Lite データベース作成メイン"""
    print("🪶 CompanyGenius Lite データベース作成スクリプト")
    print("=" * 60)
    print("データソース: EDINETコードリスト")
    print("URL: https://disclosure2.edinet-fsa.go.jp/weee0010.aspx")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("\n使用方法:")
        print("  python create_database_lite.py")
        print("\n前提条件:")
        print("  - EDINETコードリストCSVファイルが同じディレクトリにある")
        print("  - ./data/ ディレクトリへの書き込み権限")
        print("\n出力:")
        print("  ./data/corporate_lite.db (約5-10MB)")
        return
    
    builder = CompanyGeniusLiteBuilder()
    
    # 1. EDINETコードリストCSVファイル検索
    if not builder.find_edinet_csv():
        sys.exit(1)
    
    # 2. CSVファイル処理
    if not builder.process_edinet_csv():
        sys.exit(1)
    
    # 3. データベース作成
    if not builder.create_lite_database():
        sys.exit(1)
    
    print("\n✅ CompanyGenius Lite セットアップ完了")
    print("📖 詳細な使用方法: README.md")
    sys.exit(0)

if __name__ == "__main__":
    main()