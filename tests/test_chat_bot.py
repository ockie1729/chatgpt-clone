import pytest
from unittest.mock import patch
from chatgpt_clone.chat_bot import get_user_input, should_continue, CONTINUE_NODE
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