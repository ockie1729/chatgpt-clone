#!/usr/bin/env python3

import os
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

# 定数
CONTINUE_NODE = "get_user_input"


class ApiKeyError(Exception):
    """API Keyが設定されていない、または無効な場合のエラー"""
    pass


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
            raise ApiKeyError("ANTHROPIC_API_KEY environment variable is not set")
        
        self.llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            api_key=api_key
        )
    
    def create_graph(self):
        # LangGraphのワークフローを構築（ノード、エッジ、条件分岐を定義）
        workflow = StateGraph(dict)
        
        # ノードを追加
        workflow.add_node("get_user_input", get_user_input)
        workflow.add_node("generate_ai_response", generate_ai_response)
        workflow.add_node("display_response", display_response)
        
        # エントリーポイントを設定
        workflow.set_entry_point("get_user_input")
        
        # エッジを追加
        workflow.add_conditional_edges(
            "get_user_input",
            should_continue,
            {
                CONTINUE_NODE: "generate_ai_response",
                END: END
            }
        )
        workflow.add_edge("generate_ai_response", "display_response")
        workflow.add_edge("display_response", "get_user_input")
        
        self.graph = workflow.compile()
    
    def run(self):
        # チャットボットを開始し、メインループを実行
        self.setup_llm()
        self.create_graph()
        
        print("ChatGPTクローンへようこそ！")
        print("終了するには '/exit' と入力してください。")
        
        # 初期状態でllmを含める
        initial_state = {"llm": self.llm}
        
        # グラフを実行
        self.graph.invoke(initial_state)


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
    try:
        chatbot = ChatBot()
        chatbot.run()
    except KeyboardInterrupt:
        print("\n\nチャットボットを終了します。さようなら！")
    except ApiKeyError as e:
        print(f"\nAPI Key エラー: {e}")
        print("環境変数 ANTHROPIC_API_KEY を設定してください。")
    except Exception as e:
        print(f"\n予期しないエラーが発生しました: {e}")
        print("プログラムを終了します。")


if __name__ == "__main__":
    main()