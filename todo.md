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

## 実装進捗

### ✅ 完了済み機能
1. **プロジェクト構造**
   - srcレイアウトへの移行
   - uv環境での依存関係管理
   - pyproject.toml設定

2. **get_user_input()** - ユーザー入力処理
   - ユーザーからのターミナル入力受付
   - `/exit`コマンドの検出と処理
   - 戻り値: `{"user_input": str, "should_exit": bool}`
   - テスト: 通常入力、終了コマンド、スペース付き終了コマンド

3. **display_response()** - レスポンス表示
   - AIの応答をターミナルに表示
   - 戻り値: state（変更なし）
   - テスト: なし（副作用のみの単純な関数）

4. **should_continue()** - 継続判定
   - LangGraphの条件分岐ノードとして使用
   - `should_exit`フラグに基づき次のノードを決定
   - 戻り値: `CONTINUE_NODE`または`END`
   - テスト: 継続パターン、終了パターン

5. **generate_ai_response()** - Claude API通信
   - Claude APIへのリクエスト送信とレスポンス処理
   - ユーザー入力を受け取り、LLMを呼び出してAI応答を生成
   - 戻り値: `{"ai_response": str}`
   - テスト: モックLLMを使用した応答生成テスト

6. **ChatBot.setup_llm()** - Claude API設定
   - ChatAnthropic インスタンスの初期化
   - APIキーの環境変数読み込みと検証
   - カスタム例外 `ApiKeyError` によるエラーハンドリング
   - テスト: LLMインスタンス作成の確認

7. **ChatBot.create_graph()** - LangGraphワークフロー構築
   - StateGraphによるワークフロー定義
   - ノード登録: get_user_input, generate_ai_response, display_response
   - エッジ設定: 条件分岐とループ処理
   - テスト: グラフ作成とinvokeメソッド確認

8. **ChatBot.run()** と **main()** - 実行部分
   - チャットボット初期化とグラフ実行
   - エラーハンドリング: ApiKeyError, KeyboardInterrupt対応
   - ユーザーフレンドリーなメッセージ表示

### ✅ 実装完了
**基本的なChatGPTクローンが完成しました！**
- 全8テストが通過
- TDDアプローチで段階的に実装
- カスタム例外による適切なエラーハンドリング
- LangGraphによる状態管理ワークフロー