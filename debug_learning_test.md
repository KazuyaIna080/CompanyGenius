# 🔍 学習機能デバッグテスト

## テスト手順

### Step 1: 初回予測テスト
1. 「ドコモ・テクノロジ」を右クリック → 「企業名を予測」
2. **期待される結果**: 「株式会社ドコモ・テクノロジ」（既存の機械学習結果）
3. **確認ポイント**: コンソールログで `📚 Current user corrections in memory: 0 entries`

### Step 2: 修正データ送信テスト
1. 予測結果の「❌ 間違い」ボタンをクリック
2. 正しい企業名を入力: 「株式会社NTTドコモ・テクノロジ」
3. 「✅ 修正を送信」をクリック
4. **確認ポイント**: 
   - 成功メッセージが表示される
   - サーバーログで修正データの処理を確認

### Step 3: 学習結果確認テスト
1. もう一度「ドコモ・テクノロジ」を右クリック → 「企業名を予測」
2. **期待される結果**: 「株式会社NTTドコモ・テクノロジ」（学習結果）
3. **確認ポイント**: 
   - コンソールログで `📚 Current user corrections in memory: 1 entries`
   - `✅ EXACT MATCH found` メッセージ

## デバッグログ確認項目

### サーバーログ (`tail -f server.log`)

#### 初回予測時
```
🔍 Prediction request (UTF-8): 'ドコモ・テクノロジ' (len: 8)
📚 Current user corrections in memory: 0 entries
🎓 Level1 User Learning - Query: 'ドコモ・テクノロジ' -> Normalized: 'ドコモ・テクノロジ'
🎓 Available corrections: 0 entries
❌ No user learning match found for: 'ドコモ・テクノロジ'
```

#### 修正送信時
```
🔧 Before correction - User corrections count: 0
🔧 Adding user correction:
   Original Query: 'ドコモ・テクノロジ'
   Predicted Name: '株式会社ドコモ・テクノロジ'
   Correct Name: '株式会社NTTドコモ・テクノロジ'
   Normalized Query: 'ドコモ・テクノロジ'
📝 User correction successfully added to memory
📊 Total user corrections in memory: 1
🔧 After correction - User corrections count: 1
✅ Correction applied to prediction system
```

#### 2回目予測時（学習結果確認）
```
🔍 Prediction request (UTF-8): 'ドコモ・テクノロジ' (len: 8)
📚 Current user corrections in memory: 1 entries
📝 User corrections entries:
   'ドコモ・テクノロジ' -> '株式会社NTTドコモ・テクノロジ'
🎓 Level1 User Learning - Query: 'ドコモ・テクノロジ' -> Normalized: 'ドコモ・テクノロジ'
🎓 Available corrections: 1 entries
✅ EXACT MATCH found: 'ドコモ・テクノロジ' -> '株式会社NTTドコモ・テクノロジ'
```

## 問題パターンと対策

### Pattern A: 学習データがメモリに保存されない
**症状**: 修正送信後も `📚 Current user corrections in memory: 0 entries`
**原因**: `add_user_correction()`関数のエラー
**対策**: エラーログを確認し、関数を修正

### Pattern B: 2回目の予測で学習データが使われない
**症状**: 2回目予測でも元の結果が返される
**原因**: APIサーバーの新しいインスタンス作成、またはメモリクリア
**対策**: インスタンス管理を確認・修正

### Pattern C: 正規化処理の不一致
**症状**: 修正データは保存されるが、検索時にマッチしない
**原因**: 保存時と検索時の正規化結果が異なる
**対策**: 正規化ロジックを統一

## 確認コマンド

```bash
# サーバーログをリアルタイム監視
tail -f /home/kazin/claude_code/server.log

# 修正ログファイルの確認
cat /home/kazin/claude_code/corrections.log

# APIサーバープロセス確認
ps aux | grep phase15_fixed_api
```