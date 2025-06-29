#!/usr/bin/env python3

import os
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

# 定数
CONTINUE_NODE = "get_user_input"


class ChatBot:
    """チャットボットのメインクラス。LangGraphワークフローを管理する"""
    
    def __init__(self):
        # ChatAnthropic インスタンスとワークフローグラフを初期化
        self.llm = None
        self.graph = None
    
    def setup_llm(self):
        # Claude APIクライアントを設定し、APIキーの検証を行う
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            api_key=api_key
        )
    
    def create_graph(self):
        # LangGraphのワークフローを構築（ノード、エッジ、条件分岐を定義）
        pass
    
    def run(self):
        # チャットボットを開始し、メインループを実行
        pass


def get_user_input(state: Dict[str, Any]) -> Dict[str, Any]:
    # ユーザーからの入力を受け取り、/exitコマンドをチェック
    # 戻り値: {"user_input": str, "should_exit": bool}
    user_input = input("\nあなた: ").strip()
    
    if user_input == '/exit':
        return {"user_input": user_input, "should_exit": True}
    
    return {"user_input": user_input, "should_exit": False}


def generate_ai_response(state: Dict[str, Any]) -> Dict[str, Any]:
    # Claude APIにリクエストを送信し、レスポンスを取得
    # エラーハンドリングも含む
    # 戻り値: {"ai_response": str}
    llm = state["llm"]
    user_input = state["user_input"]
    
    response = llm.invoke(user_input)
    return {"ai_response": response.content}


def display_response(state: Dict[str, Any]) -> Dict[str, Any]:
    # AIの応答をターミナルに表示
    # 戻り値: state（変更なし）
    print(f"\nAI: {state['ai_response']}")
    return state


def should_continue(state: Dict[str, Any]) -> str:
    # 会話を続けるかどうかを判定
    # 戻り値: "get_user_input" または END
    if state["should_exit"]:
        return END
    return CONTINUE_NODE


def main():
    # プログラムのエントリーポイント
    # ChatBotインスタンスを作成して実行
    pass


if __name__ == "__main__":
    main()