#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 15 Week 1: FastAPI統合企業名予測サーバー - Claude Code版
6段階カスケードシステムのAPI化による商用化準備
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import sqlite3
import time
import logging
import os
from datetime import datetime
import json
from typing import Optional, Dict, Any, List
import uvicorn
import asyncio
import hashlib

# 既存の統合システムをインポート
from phase15_mega_cascade_system import MegaScaleCascadeSystem

# Linux環境での文字コード設定
os.environ['PYTHONIOENCODING'] = 'utf-8'

# FastAPIアプリケーション初期化
app = FastAPI(
    title="Enterprise Name Prediction API",
    description="6段階カスケード統合企業名予測システム API - Claude Code版",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定（開発用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では特定のドメインに制限
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# セキュリティスキーム
security = HTTPBearer(optional=True)

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/kazin/claude_code/fastapi_server.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# グローバル変数
prediction_system = None
api_stats = {
    'total_requests': 0,
    'successful_predictions': 0,
    'start_time': datetime.now(),
    'cascade_usage': {}
}

# リクエスト/レスポンスモデル
class PredictionRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=100, description="企業名検索クエリ")
    user_id: Optional[str] = Field(None, description="ユーザーID（学習機能用）")
    context: Optional[str] = Field(None, description="検索コンテキスト")
    include_alternatives: bool = Field(True, description="代替候補を含むかどうか")

class PredictionResponse(BaseModel):
    query: str
    predicted_name: str
    confidence: float
    source: str
    alternatives: List[Dict[str, Any]] = []
    prediction_time_ms: float
    timestamp: str
    system_version: str

class HealthResponse(BaseModel):
    status: str
    uptime_seconds: float
    database_size: int
    total_requests: int
    accuracy_stats: Dict[str, Any]

class UserLearningRequest(BaseModel):
    query: str = Field(..., description="検索クエリ")
    correct_name: str = Field(..., description="正しい企業名")
    user_id: Optional[str] = Field(None, description="ユーザーID")

class LearningResponse(BaseModel):
    status: str
    message: str
    learning_count: int

class BatchPredictionRequest(BaseModel):
    queries: List[str] = Field(..., max_items=50, description="企業名検索クエリのリスト")
    user_id: Optional[str] = Field(None, description="ユーザーID")

class BatchPredictionResponse(BaseModel):
    results: List[PredictionResponse]
    total_queries: int
    successful_predictions: int
    total_time_ms: float

# API Key認証（簡易版）
def verify_api_key(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """API Key認証（開発版）"""
    # 本番環境では、より厳密な認証システムを実装
    if credentials is None:
        return {"user_id": "anonymous", "tier": "free"}
    
    # 簡易的なAPI Key検証
    valid_keys = {
        "dev-key-12345": {"user_id": "developer", "tier": "premium"},
        "test-key-67890": {"user_id": "tester", "tier": "basic"},
        "claude-code-key": {"user_id": "claude_code_user", "tier": "premium"}
    }
    
    if credentials.credentials in valid_keys:
        return valid_keys[credentials.credentials]
    
    # API Keyが無効でも匿名アクセスを許可（開発用）
    return {"user_id": "anonymous", "tier": "free"}

# アプリケーション起動時の初期化
@app.on_event("startup")
async def startup_event():
    """サーバー起動時の初期化"""
    global prediction_system
    
    logger.info("Phase 15 Week 1 FastAPI サーバー起動開始 - Claude Code版")
    
    try:
        # 統合企業名予測システム初期化
        prediction_system = MegaScaleCascadeSystem()
        logger.info("6段階カスケード統合システム初期化完了")
        
        # システム統計取得
        stats = prediction_system.get_system_statistics()
        logger.info(f"システム統計: {stats}")
        
        logger.info("FastAPI サーバー起動完了")
        
    except Exception as e:
        logger.error(f"サーバー起動エラー: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """サーバー終了時の処理"""
    logger.info("FastAPI サーバー終了処理実行")

# ルートエンドポイント
@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "Enterprise Name Prediction API - Claude Code版",
        "version": "1.0.0",
        "system": "6段階カスケード統合システム",
        "docs": "/docs",
        "health": "/health",
        "environment": "Claude Code WSL2"
    }

# ヘルスチェックエンドポイント
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """システムヘルスチェック"""
    global prediction_system, api_stats
    
    uptime = (datetime.now() - api_stats['start_time']).total_seconds()
    
    try:
        # データベース接続テスト
        stats = prediction_system.get_system_statistics()
        
        health_data = {
            "status": "healthy",
            "uptime_seconds": uptime,
            "database_size": stats.get('database_size', 0),
            "total_requests": api_stats['total_requests'],
            "accuracy_stats": {
                "successful_predictions": api_stats['successful_predictions'],
                "success_rate": (api_stats['successful_predictions'] / max(api_stats['total_requests'], 1)) * 100,
                "cascade_usage": api_stats['cascade_usage']
            }
        }
        
        return HealthResponse(**health_data)
        
    except Exception as e:
        logger.error(f"ヘルスチェックエラー: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="システムヘルスチェック失敗"
        )

# メイン予測エンドポイント
@app.post("/api/v1/predict", response_model=PredictionResponse)
async def predict_company_name(
    request: PredictionRequest,
    auth: dict = Depends(verify_api_key)
):
    """企業名予測API"""
    global prediction_system, api_stats
    
    api_stats['total_requests'] += 1
    
    logger.info(f"予測リクエスト: '{request.query}' (User: {auth['user_id']})")
    
    try:
        # 予測実行
        result = prediction_system.cascade_predict(
            query=request.query,
            user_id=request.user_id or auth['user_id']
        )
        
        # 統計更新
        api_stats['successful_predictions'] += 1
        source = result.get('source', 'unknown')
        api_stats['cascade_usage'][source] = api_stats['cascade_usage'].get(source, 0) + 1
        
        # レスポンス構築
        response_data = {
            "query": request.query,
            "predicted_name": result['prediction'],
            "confidence": result['confidence'],
            "source": result['source'],
            "alternatives": [] if not request.include_alternatives else [],
            "prediction_time_ms": result['response_time_ms'],
            "timestamp": datetime.now().isoformat(),
            "system_version": "Phase15_Claude_Code_v1.0"
        }
        
        logger.info(f"予測完了: {result['prediction']} ({result['confidence']:.3f})")
        
        return PredictionResponse(**response_data)
        
    except Exception as e:
        logger.error(f"予測エラー: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"企業名予測エラー: {str(e)}"
        )

# バッチ予測エンドポイント
@app.post("/api/v1/predict/batch", response_model=BatchPredictionResponse)
async def batch_predict(
    request: BatchPredictionRequest,
    auth: dict = Depends(verify_api_key)
):
    """バッチ企業名予測API"""
    global prediction_system, api_stats
    
    # プレミアムユーザーのみバッチ処理可能
    if auth['tier'] == 'free' and len(request.queries) > 10:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="フリープランは10件まで。プレミアムプランにアップグレードしてください。"
        )
    
    logger.info(f"バッチ予測リクエスト: {len(request.queries)}件 (User: {auth['user_id']})")
    
    start_time = time.time()
    results = []
    successful_count = 0
    
    try:
        for query in request.queries:
            api_stats['total_requests'] += 1
            
            try:
                result = prediction_system.cascade_predict(
                    query=query,
                    user_id=request.user_id or auth['user_id']
                )
                
                response_data = {
                    "query": query,
                    "predicted_name": result['prediction'],
                    "confidence": result['confidence'],
                    "source": result['source'],
                    "alternatives": [],
                    "prediction_time_ms": result['response_time_ms'],
                    "timestamp": datetime.now().isoformat(),
                    "system_version": "Phase15_Claude_Code_v1.0"
                }
                
                results.append(PredictionResponse(**response_data))
                successful_count += 1
                api_stats['successful_predictions'] += 1
                
                # カスケード統計更新
                source = result.get('source', 'unknown')
                api_stats['cascade_usage'][source] = api_stats['cascade_usage'].get(source, 0) + 1
                
            except Exception as e:
                logger.warning(f"バッチ予測個別エラー '{query}': {e}")
                # エラーの場合もレスポンスに含める
                error_response = {
                    "query": query,
                    "predicted_name": f"エラー: {str(e)}",
                    "confidence": 0.0,
                    "source": "error",
                    "alternatives": [],
                    "prediction_time_ms": 0.0,
                    "timestamp": datetime.now().isoformat(),
                    "system_version": "error"
                }
                results.append(PredictionResponse(**error_response))
        
        total_time = (time.time() - start_time) * 1000
        
        response_data = {
            "results": results,
            "total_queries": len(request.queries),
            "successful_predictions": successful_count,
            "total_time_ms": total_time
        }
        
        logger.info(f"バッチ予測完了: {successful_count}/{len(request.queries)} 成功")
        
        return BatchPredictionResponse(**response_data)
        
    except Exception as e:
        logger.error(f"バッチ予測エラー: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"バッチ予測エラー: {str(e)}"
        )

# システム統計エンドポイント
@app.get("/api/v1/stats")
async def get_system_stats(auth: dict = Depends(verify_api_key)):
    """システム統計情報取得"""
    global prediction_system, api_stats
    
    try:
        system_stats = prediction_system.get_system_statistics()
        uptime = (datetime.now() - api_stats['start_time']).total_seconds()
        
        stats = {
            "system_info": system_stats,
            "api_stats": {
                "uptime_seconds": uptime,
                "total_requests": api_stats['total_requests'],
                "successful_predictions": api_stats['successful_predictions'],
                "success_rate": (api_stats['successful_predictions'] / max(api_stats['total_requests'], 1)) * 100,
                "cascade_usage": api_stats['cascade_usage']
            },
            "environment": "Claude Code WSL2",
            "timestamp": datetime.now().isoformat()
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"統計取得エラー: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"統計取得エラー: {str(e)}"
        )

# ベンチマークエンドポイント（開発用）
@app.get("/api/v1/benchmark")
async def run_benchmark(auth: dict = Depends(verify_api_key)):
    """システムベンチマーク実行（開発用）"""
    
    try:
        logger.info("システムベンチマーク開始")
        
        # テストケース
        test_cases = [
            ("トヨタ", "トヨタ自動車株式会社"),
            ("ソニー", "ソニー株式会社"),
            ("ソフトバンク", "ソフトバンクグループ株式会社"),
            ("ユニクロ", "株式会社ファーストリテイリング"),
            ("マック", "日本マクドナルド株式会社"),
            ("楽天", "楽天グループ株式会社"),
            ("KDDI", "KDDI株式会社"),
            ("NTT", "日本電信電話株式会社")
        ]
        
        benchmark_result = prediction_system.benchmark_mega_system(test_cases)
        
        logger.info(f"ベンチマーク完了: 精度 {benchmark_result['accuracy']:.1f}%")
        
        return {
            "status": "completed",
            "benchmark_result": benchmark_result,
            "timestamp": datetime.now().isoformat(),
            "environment": "Claude Code WSL2"
        }
        
    except Exception as e:
        logger.error(f"ベンチマークエラー: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ベンチマークエラー: {str(e)}"
        )

# サーバー起動関数
def run_server():
    """サーバー起動"""
    logger.info("Phase 15 Week 1 FastAPI サーバー起動 - Claude Code版")
    
    uvicorn.run(
        "phase15_fastapi_server:app",
        host="127.0.0.1",
        port=8000,
        reload=True,  # 開発環境では True
        log_level="info"
    )

if __name__ == "__main__":
    run_server()