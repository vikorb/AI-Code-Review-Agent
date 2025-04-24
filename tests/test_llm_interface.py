"""
Unit tests for the LLMClient class.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.llm_interface import LLMClient


class TestLLMClient(unittest.TestCase):
    """Tests for the LLMClient class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a test config
        self.test_config = {
            "api_keys": {
                "openai": "test_openai_key",
                "anthropic": "test_anthropic_key"
            }
        }
        
        # Mock the config loading
        self.config_patcher = patch('agent.llm_interface.LLMClient._load_config')
        self.mock_load_config = self.config_patcher.start()
        self.mock_load_config.return_value = self.test_config
        
        # Mock the client imports
        self.openai_patcher = patch('openai.OpenAI')
        self.mock_openai = self.openai_patcher.start()
        
        self.anthropic_patcher = patch('anthropic.Anthropic')
        self.mock_anthropic = self.anthropic_patcher.start()
        
        # Mock requests for Ollama
        self.requests_patcher = patch('agent.llm_interface.requests')
        self.mock_requests = self.requests_patcher.start()
        
        # Set up the response for Ollama
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"response": "This is a test response"}\n'
        self.mock_requests.post.return_value = mock_response
    
    def tearDown(self):
        """Tear down test environment."""
        self.config_patcher.stop()
        self.openai_patcher.stop()
        self.anthropic_patcher.stop()
        self.requests_patcher.stop()
    
    def test_init_openai(self):
        """Test initialization with OpenAI provider."""
        client = LLMClient("openai", "gpt-4")
        self.assertEqual(client.provider, "openai")
        self.assertEqual(client.model, "gpt-4")
        self.mock_openai.assert_called_once()
    
    def test_init_anthropic(self):
        """Test initialization with Anthropic provider."""
        client = LLMClient("anthropic", "claude-3")
        self.assertEqual(client.provider, "anthropic")
        self.assertEqual(client.model, "claude-3")
        self.mock_anthropic.assert_called_once()
    
    def test_init_ollama(self):
        """Test initialization with Ollama provider."""
        client = LLMClient("ollama", "mistral")
        self.assertEqual(client.provider, "ollama")
        self.assertEqual(client.model, "mistral")
    
    def test_init_invalid_provider(self):
        """Test initialization with an invalid provider."""
        with self.assertRaises(ValueError):
            LLMClient("invalid", "model")
    
    def test_get_api_key_from_config(self):
        """Test getting API key from config."""
        client = LLMClient("openai", "gpt-4")
        key = client._get_api_key("openai")
        self.assertEqual(key, "test_openai_key")
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "env_test_key"})
    def test_get_api_key_from_env(self):
        """Test getting API key from environment variable."""
        # Remove the key from config
        config_without_openai = {
            "api_keys": {
                "anthropic": "test_anthropic_key"
            }
        }
        self.mock_load_config.return_value = config_without_openai
        
        client = LLMClient("openai", "gpt-4")
        key = client._get_api_key("openai")
        self.assertEqual(key, "env_test_key")
    
    def test_get_api_key_missing(self):
        """Test error when API key is missing."""
        # Remove all API keys
        self.mock_load_config.return_value = {"api_keys": {}}
        
        client = LLMClient("openai", "gpt-4")
        with self.assertRaises(ValueError):
            client._get_api_key("openai")
    
    def test_call_openai(self):
        """Test calling the OpenAI API."""
        # Mock the OpenAI client response
        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Test OpenAI response"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        
        self.mock_openai.return_value.chat.completions.create.return_value = mock_completion
        
        client = LLMClient("openai", "gpt-4")
        response = client._call_openai("Test system prompt", "Test user prompt")
        
        self.assertEqual(response, "Test OpenAI response")
        self.mock_openai.return_value.chat.completions.create.assert_called_once()
    
    def test_call_anthropic(self):
        """Test calling the Anthropic Claude API."""
        # Mock the Anthropic client response
        mock_content = MagicMock()
        mock_content.text = "Test Anthropic response"
        mock_response = MagicMock()
        mock_response.content = [mock_content]
        
        self.mock_anthropic.return_value.messages.create.return_value = mock_response
        
        client = LLMClient("anthropic", "claude-3")
        response = client._call_anthropic("Test system prompt", "Test user prompt")
        
        self.assertEqual(response, "Test Anthropic response")
        self.mock_anthropic.return_value.messages.create.assert_called_once()
    
    def test_call_ollama(self):
        """Test calling the Ollama API."""
        client = LLMClient("ollama", "mistral")
        response = client._call_ollama("Test system prompt", "Test user prompt")
        
        self.assertEqual(response, "This is a test response")
        self.mock_requests.post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": "<s>\nTest system prompt\n</s>\n\nTest user prompt",
                "temperature": 0.1,
                "system": "Test system prompt",
            },
            headers={"Content-Type": "application/json"}
        )
    
    def test_run(self):
        """Test the run method with different providers."""
        # Mock the individual call methods
        with patch.object(LLMClient, '_call_openai', return_value="OpenAI response") as mock_openai_call:
            client_openai = LLMClient("openai", "gpt-4")
            response_openai = client_openai.run("System", "User", "code")
            self.assertEqual(response_openai, "OpenAI response")
            mock_openai_call.assert_called_once()
        
        with patch.object(LLMClient, '_call_anthropic', return_value="Anthropic response") as mock_anthropic_call:
            client_anthropic = LLMClient("anthropic", "claude-3")
            response_anthropic = client_anthropic.run("System", "User", "code")
            self.assertEqual(response_anthropic, "Anthropic response")
            mock_anthropic_call.assert_called_once()
        
        with patch.object(LLMClient, '_call_ollama', return_value="Ollama response") as mock_ollama_call:
            client_ollama = LLMClient("ollama", "mistral")
            response_ollama = client_ollama.run("System", "User", "code")
            self.assertEqual(response_ollama, "Ollama response")
            mock_ollama_call.assert_called_once()


if __name__ == '__main__':
    unittest.main()