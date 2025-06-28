# ChatGPTクローン設計

## 要件
- ターミナルベースのシンプルなチャットアプリケーション
- Claude APIを使用
- 単発の会話（セッション管理不要）
- 認証機能なし
- 終了コマンドあり

## 技術スタック
- Python
- LangGraph（状態管理とワークフロー制御）
- Anthropic Claude API
- LangChain（LLMインテグレーション）

## 基本仕様
1. プログラム起動
2. ユーザーからの入力を受け取る
3. LangGraphでワークフローを管理
4. Claude APIに送信して応答を取得
5. 応答を表示
6. 終了コマンド（exit, quit等）まで2-5を繰り返し

## LangGraphアーキテクチャ
- State: ユーザー入力、AI応答を管理
- Nodes: ユーザー入力処理、AI応答生成、出力表示
- Edges: 各ノード間の遷移ロジック

## 実装方針
- LangGraphを活用した状態管理
- エラーハンドリング
- API キーの環境変数管理