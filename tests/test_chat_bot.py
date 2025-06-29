import pytest
from unittest.mock import patch, Mock
from chatgpt_clone.chat_bot import get_user_input, should_continue, generate_ai_response, ChatBot, CONTINUE_NODE
from langgraph.graph import END


class TestGetUserInput:
    """get_user_input関数のテストクラス"""
    
    @patch('builtins.input', return_value='こんにちは')
    def test_normal_input(self, mock_input):
        """通常の入力をテスト"""
        result = get_user_input({})
        assert result == {"user_input": "こんにちは", "should_exit": False}
    
    @patch('builtins.input', return_value='/exit')
    def test_exit_command(self, mock_input):
        """終了コマンドをテスト"""
        result = get_user_input({})
        assert result == {"user_input": "/exit", "should_exit": True}
    
    @patch('builtins.input', return_value='  /exit  ')
    def test_exit_command_with_spaces(self, mock_input):
        """前後にスペースがある終了コマンドをテスト"""
        result = get_user_input({})
        assert result == {"user_input": "/exit", "should_exit": True}


class TestShouldContinue:
    """should_continue関数のテストクラス"""
    
    def test_should_continue_when_no_exit(self):
        """終了フラグがない場合は継続"""
        state = {"should_exit": False}
        result = should_continue(state)
        assert result == CONTINUE_NODE
    
    def test_should_exit_when_exit_flag_true(self):
        """終了フラグがある場合は終了"""
        state = {"should_exit": True}
        result = should_continue(state)
        assert result == END


class TestGenerateAiResponse:
    """generate_ai_response関数のテストクラス"""
    
    def test_generate_ai_response_returns_response(self):
        """AI応答を正しく返すことをテスト"""
        mock_llm = Mock()
        mock_llm.invoke.return_value.content = "こんにちは！何をお手伝いしましょうか？"
        
        state = {
            "user_input": "こんにちは",
            "llm": mock_llm
        }
        
        result = generate_ai_response(state)
        assert result == {"ai_response": "こんにちは！何をお手伝いしましょうか？"}


class TestChatBot:
    """ChatBotクラスのテストクラス"""
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-api-key'})
    def test_setup_llm_creates_chat_anthropic(self):
        """setup_llm()がChatAnthropicインスタンスを作成することをテスト"""
        chatbot = ChatBot()
        chatbot.setup_llm()
        
        assert chatbot.llm is not None
        assert hasattr(chatbot.llm, 'invoke')