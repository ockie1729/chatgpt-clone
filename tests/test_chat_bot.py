import pytest
from unittest.mock import patch
from chatgpt_clone.chat_bot import get_user_input


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