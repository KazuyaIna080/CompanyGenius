#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 15 Week 1: システム動作確認・テストスクリプト - Claude Code版
FastAPI + Chrome拡張統合の包括的テスト
"""

import sys
import os
import time
import json
import asyncio
import subprocess
import requests
from datetime import datetime
import sqlite3

# 既存システムのパスを追加
sys.path.append(os.path.dirname(__file__))

# Linux環境での文字コード設定
os.environ['PYTHONIOENCODING'] = 'utf-8'

class Phase15SystemTester:
    """Phase 15システム統合テスター - Claude Code版"""
    
    def __init__(self):
        self.test_results = {
            'start_time': datetime.now(),
            'tests': [],
            'summary': {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'errors': []
            }
        }
        
        self.api_url = "http://127.0.0.1:8000"
        self.db_path = "/mnt/c/Users/kazin/Desktop/corporate_phase2_stable.db"
        
    def log_test(self, test_name, success, details=None):
        """テスト結果ログ"""
        result = {
            'name': test_name,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        
        self.test_results['tests'].append(result)
        self.test_results['summary']['total'] += 1
        
        if success:
            self.test_results['summary']['passed'] += 1
            print(f"✅ {test_name}: PASSED")
        else:
            self.test_results['summary']['failed'] += 1
            print(f"❌ {test_name}: FAILED")
            if details:
                print(f"   Details: {details}")
                self.test_results['summary']['errors'].append({
                    'test': test_name,
                    'error': details
                })

    def test_database_connection(self):
        """データベース接続テスト"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 基本クエリテスト
            cursor.execute("SELECT COUNT(*) FROM corporate_master")
            count = cursor.fetchone()[0]
            
            # サンプルデータ取得
            cursor.execute("SELECT name FROM corporate_master LIMIT 5")
            samples = cursor.fetchall()
            
            conn.close()
            
            self.log_test(
                "Database Connection", 
                True, 
                f"Database contains {count:,} companies"
            )
            
            return True
            
        except Exception as e:
            self.log_test("Database Connection", False, str(e))
            return False

    def test_core_system_import(self):
        """中核システムインポートテスト"""
        try:
            from phase15_mega_cascade_system import MegaScaleCascadeSystem
            
            # システム初期化
            system = MegaScaleCascadeSystem()
            
            self.log_test("Core System Import", True, "System initialized successfully")
            return system
            
        except Exception as e:
            self.log_test("Core System Import", False, str(e))
            return None

    def test_cascade_prediction(self, system):
        """カスケード予測テスト"""
        if not system:
            self.log_test("Cascade Prediction", False, "System not available")
            return False
        
        try:
            test_queries = [
                "トヨタ",
                "ソニー", 
                "テスト商事",
                "マック"
            ]
            
            all_passed = True
            results = []
            
            for query in test_queries:
                result = system.cascade_predict(query)
                
                prediction_ok = (
                    'prediction' in result and 
                    'confidence' in result and 
                    'source' in result and
                    result['confidence'] > 0
                )
                
                if prediction_ok:
                    results.append(f"{query} -> {result['prediction']} ({result['confidence']:.3f})")
                else:
                    all_passed = False
                    results.append(f"{query} -> ERROR")
            
            self.log_test(
                "Cascade Prediction", 
                all_passed, 
                f"Tested {len(test_queries)} queries: {'; '.join(results)}"
            )
            
            return all_passed
            
        except Exception as e:
            self.log_test("Cascade Prediction", False, str(e))
            return False

    def test_api_server_health(self):
        """APIサーバーヘルスチェック"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                self.log_test(
                    "API Server Health", 
                    True, 
                    f"Status: {health_data.get('status', 'unknown')}, DB Size: {health_data.get('database_size', 0):,}"
                )
                return True
            else:
                self.log_test("API Server Health", False, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.log_test("API Server Health", False, "Connection refused - server not running")
            return False
        except Exception as e:
            self.log_test("API Server Health", False, str(e))
            return False

    def test_api_prediction(self):
        """API予測エンドポイントテスト"""
        try:
            test_data = {
                "query": "トヨタ",
                "user_id": "test_user",
                "include_alternatives": True
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer claude-code-key'
            }
            
            response = requests.post(
                f"{self.api_url}/api/v1/predict", 
                json=test_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                prediction_ok = (
                    'predicted_name' in result and 
                    'confidence' in result and 
                    result['confidence'] > 0
                )
                
                if prediction_ok:
                    self.log_test(
                        "API Prediction", 
                        True, 
                        f"'{test_data['query']}' -> '{result['predicted_name']}' ({result['confidence']:.3f})"
                    )
                    return True
                else:
                    self.log_test("API Prediction", False, "Invalid response format")
                    return False
            else:
                self.log_test("API Prediction", False, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.log_test("API Prediction", False, "Connection refused - server not running")
            return False
        except Exception as e:
            self.log_test("API Prediction", False, str(e))
            return False

    def test_batch_prediction(self):
        """バッチ予測テスト"""
        try:
            test_data = {
                "queries": ["トヨタ", "ソニー", "楽天"],
                "user_id": "test_user"
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer claude-code-key'
            }
            
            response = requests.post(
                f"{self.api_url}/api/v1/predict/batch", 
                json=test_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                batch_ok = (
                    'results' in result and 
                    'total_queries' in result and 
                    len(result['results']) == len(test_data['queries'])
                )
                
                if batch_ok:
                    successful = result.get('successful_predictions', 0)
                    self.log_test(
                        "Batch Prediction", 
                        True, 
                        f"Processed {result['total_queries']} queries, {successful} successful"
                    )
                    return True
                else:
                    self.log_test("Batch Prediction", False, "Invalid batch response format")
                    return False
            else:
                self.log_test("Batch Prediction", False, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            self.log_test("Batch Prediction", False, "Connection refused - server not running")
            return False
        except Exception as e:
            self.log_test("Batch Prediction", False, str(e))
            return False

    def test_chrome_extension_files(self):
        """Chrome拡張機能ファイルテスト"""
        try:
            extension_dir = "/home/kazin/claude_code/chrome_extension"
            required_files = [
                "manifest.json",
                "background.js", 
                "content.js",
                "popup.html",
                "popup.js"
            ]
            
            missing_files = []
            for file in required_files:
                file_path = os.path.join(extension_dir, file)
                if not os.path.exists(file_path):
                    missing_files.append(file)
            
            if not missing_files:
                self.log_test(
                    "Chrome Extension Files", 
                    True, 
                    f"All {len(required_files)} files present"
                )
                return True
            else:
                self.log_test(
                    "Chrome Extension Files", 
                    False, 
                    f"Missing files: {', '.join(missing_files)}"
                )
                return False
                
        except Exception as e:
            self.log_test("Chrome Extension Files", False, str(e))
            return False

    def run_performance_benchmark(self, system):
        """パフォーマンスベンチマーク"""
        if not system:
            self.log_test("Performance Benchmark", False, "System not available")
            return False
        
        try:
            test_cases = [
                ("トヨタ", "トヨタ自動車株式会社"),
                ("ソニー", "ソニー株式会社"),
                ("ソフトバンク", "ソフトバンクグループ株式会社"),
                ("楽天", "楽天グループ株式会社"),
                ("KDDI", "KDDI株式会社")
            ]
            
            benchmark_result = system.benchmark_mega_system(test_cases)
            
            performance_ok = (
                benchmark_result['accuracy'] >= 80 and  # 最低80%精度
                benchmark_result['performance_stats']['avg_response_time'] < 100  # 100ms以下
            )
            
            if performance_ok:
                self.log_test(
                    "Performance Benchmark", 
                    True, 
                    f"Accuracy: {benchmark_result['accuracy']:.1f}%, Avg Response: {benchmark_result['performance_stats']['avg_response_time']:.1f}ms"
                )
                return True
            else:
                self.log_test(
                    "Performance Benchmark", 
                    False, 
                    f"Performance below threshold - Accuracy: {benchmark_result['accuracy']:.1f}%, Response: {benchmark_result['performance_stats']['avg_response_time']:.1f}ms"
                )
                return False
                
        except Exception as e:
            self.log_test("Performance Benchmark", False, str(e))
            return False

    def run_all_tests(self):
        """全テスト実行"""
        print("=" * 60)
        print("Phase 15 System Integration Test - Claude Code版")
        print("=" * 60)
        print(f"Test Start: {self.test_results['start_time']}")
        print()
        
        # 1. データベース接続テスト
        self.test_database_connection()
        
        # 2. 中核システムテスト
        system = self.test_core_system_import()
        
        # 3. カスケード予測テスト
        self.test_cascade_prediction(system)
        
        # 4. APIサーバーテスト
        self.test_api_server_health()
        self.test_api_prediction()
        self.test_batch_prediction()
        
        # 5. Chrome拡張機能ファイルテスト
        self.test_chrome_extension_files()
        
        # 6. パフォーマンステスト
        self.run_performance_benchmark(system)
        
        # 結果サマリー
        self.print_test_summary()
        
        return self.test_results

    def print_test_summary(self):
        """テストサマリー出力"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        summary = self.test_results['summary']
        end_time = datetime.now()
        duration = (end_time - self.test_results['start_time']).total_seconds()
        
        print(f"Total Tests: {summary['total']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success Rate: {summary['passed']/summary['total']*100:.1f}%")
        print(f"Duration: {duration:.1f} seconds")
        
        if summary['failed'] > 0:
            print(f"\nFailed Tests:")
            for error in summary['errors']:
                print(f"  - {error['test']}: {error['error']}")
        
        print(f"\nTest End: {end_time}")
        print("=" * 60)

    def save_test_report(self):
        """テストレポート保存"""
        report_file = f"/home/kazin/claude_code/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, ensure_ascii=False, indent=2, default=str)
            
            print(f"\n📄 Test report saved: {report_file}")
            return report_file
            
        except Exception as e:
            print(f"❌ Failed to save test report: {e}")
            return None

def main():
    """メイン実行"""
    tester = Phase15SystemTester()
    
    # 全テスト実行
    results = tester.run_all_tests()
    
    # レポート保存
    tester.save_test_report()
    
    # 終了コード
    if results['summary']['failed'] == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {results['summary']['failed']} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(main())