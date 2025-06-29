# ChatGPT Clone

ターミナルベースのシンプルなチャットアプリケーション。Claude APIとLangGraphを使用しています。

## 機能

- ターミナルでのインタラクティブなチャット
- Claude APIによるAI応答生成
- LangGraphを使った状態管理ワークフロー
- 終了コマンド (`/exit`) サポート
- 適切なエラーハンドリング

## 技術スタック

- **Python** >= 3.9
- **LangGraph** - 状態管理とワークフロー制御
- **LangChain** - LLMインテグレーション
- **Anthropic Claude API** - AI応答生成
- **uv** - 依存関係管理

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/ockie1729/chatgpt-clone.git
cd chatgpt-clone
```

### 2. 依存関係のインストール

```bash
uv sync
```

### 3. 環境変数の設定

`.env`ファイルを作成し、Anthropic API Keyを設定します：

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

## 使用方法

```bash
uv run python src/chatgpt_clone/chat_bot.py
```

チャットが開始されたら、メッセージを入力してEnterを押してください。
終了するには `/exit` と入力します。

## 開発

### テストの実行

```bash
uv run pytest
```