#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CompanyGenius データベース作成スクリプト
法人番号公表システムのCSVファイルからSQLiteデータベースを作成
"""

import sqlite3
import csv
import os
import sys
from datetime import datetime

def create_corporate_database():
    """法人番号CSVからSQLiteデータベースを作成"""
    
    print("🧠 CompanyGenius データベース作成スクリプト")
    print("=" * 50)
    
    # CSVファイルのパスを確認
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and ('houjin' in f.lower() or 'corporate' in f.lower())]
    if not csv_files:
        print("❌ 法人番号CSVファイルが見つかりません")
        print()
        print("📥 ダウンロード手順:")
        print("1. https://www.houjin-bangou.nta.go.jp/download/ にアクセス")
        print("2. 「全件データ」をダウンロード")
        print("3. ZIPファイルを解凍してCSVファイルをこのディレクトリに配置")
        print("4. 再度このスクリプトを実行")
        return False
    
    csv_file = csv_files[0]
    db_dir = './data'
    db_path = os.path.join(db_dir, 'corporate_phase2_stable.db')
    
    # データディレクトリ作成
    os.makedirs(db_dir, exist_ok=True)
    
    print(f"📊 入力CSVファイル: {csv_file}")
    print(f"📁 出力データベース: {db_path}")
    
    # ファイルサイズ確認
    csv_size = os.path.getsize(csv_file) / (1024**3)  # GB
    print(f"📈 CSVファイルサイズ: {csv_size:.2f} GB")
    
    if csv_size > 5:
        print("⚠️  大容量ファイルです。処理に時間がかかる可能性があります")
    
    # 既存データベースの確認
    if os.path.exists(db_path):
        response = input(f"⚠️  既存のデータベースが見つかりました: {db_path}\n上書きしますか？ (y/N): ")
        if response.lower() not in ['y', 'yes']:
            print("❌ 処理を中止しました")
            return False
        os.remove(db_path)
    
    print("\n🔧 データベース作成開始...")
    start_time = datetime.now()
    
    try:
        # SQLiteデータベース作成
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # テーブル作成
        cursor.execute('''
            CREATE TABLE companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                corporate_number TEXT UNIQUE,
                process_type TEXT,
                correct_flag TEXT,
                update_date TEXT,
                change_date TEXT,
                company_name TEXT,
                company_name_kana TEXT,
                prefecture_code TEXT,
                city_code TEXT,
                street_address TEXT,
                business_category TEXT,
                capital TEXT,
                employee_count TEXT,
                status TEXT,
                close_date TEXT,
                close_reason TEXT,
                successor_corporate_number TEXT,
                change_reason TEXT,
                assignment_date TEXT,
                latest_update_date TEXT,
                en_company_name TEXT,
                en_address_line TEXT,
                en_prefecture_name TEXT,
                en_city_name TEXT,
                en_address_outside_city TEXT,
                nearest_station TEXT
            )
        ''')
        
        print("✅ テーブル作成完了")
        
        # CSVデータ読み込み
        print("📥 CSVデータ読み込み中...")
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            # CSVの区切り文字を自動検出
            sample = f.read(1024)
            f.seek(0)
            
            # 一般的な区切り文字を試行
            if '\t' in sample:
                delimiter = '\t'
            elif ',' in sample:
                delimiter = ','
            else:
                delimiter = ','
            
            reader = csv.reader(f, delimiter=delimiter)
            
            try:
                header = next(reader)  # ヘッダーをスキップ
                print(f"📋 ヘッダー列数: {len(header)}")
            except StopIteration:
                print("❌ CSVファイルが空です")
                return False
            
            batch_size = 10000
            batch_data = []
            count = 0
            error_count = 0
            
            for row_num, row in enumerate(reader, start=2):  # ヘッダーを除いて2行目から
                try:
                    # データの長さを調整（不足分は空文字で埋める）
                    adjusted_row = row[:27] + [''] * (27 - len(row[:27]))
                    batch_data.append(adjusted_row)
                    count += 1
                    
                    # バッチサイズに達したらデータベースに挿入
                    if len(batch_data) >= batch_size:
                        cursor.executemany('''
                            INSERT OR IGNORE INTO companies (
                                corporate_number, process_type, correct_flag, update_date, 
                                change_date, company_name, company_name_kana, prefecture_code, 
                                city_code, street_address, business_category, capital, 
                                employee_count, status, close_date, close_reason, 
                                successor_corporate_number, change_reason, assignment_date, 
                                latest_update_date, en_company_name, en_address_line, 
                                en_prefecture_name, en_city_name, en_address_outside_city, 
                                nearest_station
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', [row[1:] for row in batch_data])  # IDを除いた25列
                        conn.commit()
                        batch_data = []
                        print(f"  📈 {count:,} 件処理完了 ({datetime.now() - start_time})")
                
                except Exception as e:
                    error_count += 1
                    if error_count <= 10:  # 最初の10エラーのみ表示
                        print(f"  ⚠️  行 {row_num} でエラー: {str(e)[:100]}")
                    continue
            
            # 残りのデータを挿入
            if batch_data:
                cursor.executemany('''
                    INSERT OR IGNORE INTO companies (
                        corporate_number, process_type, correct_flag, update_date, 
                        change_date, company_name, company_name_kana, prefecture_code, 
                        city_code, street_address, business_category, capital, 
                        employee_count, status, close_date, close_reason, 
                        successor_corporate_number, change_reason, assignment_date, 
                        latest_update_date, en_company_name, en_address_line, 
                        en_prefecture_name, en_city_name, en_address_outside_city, 
                        nearest_station
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', [row[1:] for row in batch_data])
                conn.commit()
        
        print(f"📊 データ挿入完了: {count:,} 件")
        if error_count > 0:
            print(f"⚠️  エラー行数: {error_count} 件")
        
        # インデックス作成（検索高速化）
        print("🔍 インデックス作成中...")
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_company_name ON companies(company_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_corporate_number ON companies(corporate_number)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_company_name_kana ON companies(company_name_kana)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON companies(status)')
        
        print("✅ インデックス作成完了")
        
        # 統計情報取得
        cursor.execute('SELECT COUNT(*) FROM companies')
        total_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT company_name) FROM companies')
        unique_names = cursor.fetchone()[0]
        
        conn.close()
        
        # 完了報告
        end_time = datetime.now()
        duration = end_time - start_time
        db_size = os.path.getsize(db_path) / (1024**2)  # MB
        
        print("\n" + "=" * 50)
        print("🎉 データベース作成完了！")
        print(f"📁 ファイル: {db_path}")
        print(f"📊 総レコード数: {total_count:,} 件")
        print(f"🏢 ユニーク企業名: {unique_names:,} 件")
        print(f"💾 データベースサイズ: {db_size:.1f} MB")
        print(f"⏱️  処理時間: {duration}")
        print("\n🚀 CompanyGenius APIサーバーを起動できます:")
        print("   python phase15_fixed_api.py")
        
        return True
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")
        if 'conn' in locals():
            conn.close()
        if os.path.exists(db_path):
            os.remove(db_path)
        return False

def main():
    """メイン関数"""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("CompanyGenius データベース作成スクリプト")
        print("")
        print("使用方法:")
        print("  python create_database.py")
        print("")
        print("前提条件:")
        print("  - 法人番号公表システムのCSVファイルが同じディレクトリにある")
        print("  - ./data/ ディレクトリへの書き込み権限")
        print("")
        print("出力:")
        print("  ./data/corporate_phase2_stable.db")
        return
    
    success = create_corporate_database()
    
    if success:
        print("\n✅ セットアップ完了")
        print("📖 詳細な使用方法: INSTALLATION_COMPLETE_GUIDE.md")
        sys.exit(0)
    else:
        print("\n❌ セットアップ失敗")
        sys.exit(1)

if __name__ == "__main__":
    main()