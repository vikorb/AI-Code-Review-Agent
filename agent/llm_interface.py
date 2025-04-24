"""
LLM Interface module for the Code Review Agent.

This module abstracts the interaction with different LLM providers
(OpenAI, Anthropic Claude, Ollama).
"""

import os
import logging
import yaml
import requests
import json
from typing import Dict, Optional, Any, Union

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMClient:
    """Client to interact with different LLM providers."""
    
    def __init__(self, provider: str, model: str, config_path: str = None):
        """
        Initialize the LLM client.
        
        Args:
            provider: The LLM provider ('openai', 'anthropic', 'ollama')
            model: The model to use
            config_path: Path to the config file containing API keys
        """
        self.provider = provider.lower()
        self.model = model
        self.config = self._load_config(config_path)
        
        # Validate provider
        valid_providers = ["openai", "anthropic", "ollama"]
        if self.provider not in valid_providers:
            raise ValueError(f"Provider must be one of {valid_providers}")
        
        # Import necessary libraries based on provider
        if self.provider == "openai":
            try:
                import openai
                self.client = openai.OpenAI(api_key=self._get_api_key("openai"))
            except ImportError:
                raise ImportError("OpenAI package not installed. Install with 'pip install openai'")
        
        elif self.provider == "anthropic":
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self._get_api_key("anthropic"))
            except ImportError:
                raise ImportError("Anthropic package not installed. Install with 'pip install anthropic'")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from a YAML file."""
        if not config_path:
            # Look for config.yaml in the project root
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
        
        try:
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found at {config_path}. Using environment variables.")
            return {}
    
    def _get_api_key(self, provider: str) -> str:
        """Get API key from config or environment variables."""
        # First check environment variables
        env_var_name = f"{provider.upper()}_API_KEY"
        api_key = os.environ.get(env_var_name)
        
        # If not in environment, try config file
        if not api_key and self.config and "api_keys" in self.config:
            api_key = self.config.get("api_keys", {}).get(provider)
        
        if not api_key:
            raise ValueError(
                f"{provider.capitalize()} API key not found. "
                f"Set it in the config file or as an environment variable {env_var_name}"
            )
        
        return api_key
    
    def run(self, system_prompt: str, user_prompt: str, code_snippet: str) -> str:
        """
        Run the LLM with the provided prompts and code.
        
        Args:
            system_prompt: The system prompt for the LLM
            user_prompt: Additional user context
            code_snippet: The code to review
        
        Returns:
            The LLM's response as a string
        """
        full_user_prompt = f"{user_prompt}\n\n```python\n{code_snippet}\n```"
        
        if self.provider == "openai":
            return self._call_openai(system_prompt, full_user_prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(system_prompt, full_user_prompt)
        elif self.provider == "ollama":
            return self._call_ollama(system_prompt, full_user_prompt)
        
        raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        """Call the OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature for code review
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            raise
    
    def _call_anthropic(self, system_prompt: str, user_prompt: str) -> str:
        """Call the Anthropic Claude API."""
        try:
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error calling Anthropic API: {e}")
            raise
    
    def _call_ollama(self, system_prompt: str, user_prompt: str) -> str:
        """Call the Ollama API (local)."""
        try:
            # Ollama format is different, merge the prompts
            combined_prompt = f"<system>\n{system_prompt}\n</system>\n\n{user_prompt}"
            
            # Assuming Ollama is running locally on default port
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model,
                    "prompt": combined_prompt,
                    "temperature": 0.1,
                    "system": system_prompt,
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                raise Exception(f"Error from Ollama API: {response.text}")
            
            # Parse streaming response (Ollama returns line-by-line JSON)
            full_response = ""
            for line in response.text.strip().split('\n'):
                if not line:
                    continue
                try:
                    resp_json = json.loads(line)
                    if "response" in resp_json:
                        full_response += resp_json["response"]
                except json.JSONDecodeError:
                    logger.warning(f"Could not parse Ollama response line: {line}")
            
            return full_response
        except Exception as e:
            logger.error(f"Error calling Ollama API: {e}")
            raise


# For testing purposes
if __name__ == "__main__":
    # Sample test
    try:
        client = LLMClient("openai", "gpt-4")
        response = client.run(
            "You are a Python code reviewer. Provide feedback on the following code.",
            "Please review this code:",
            "def add(a, b):\n    return a + b"
        )
        print(response)
    except Exception as e:
        logger.error(f"Test failed: {e}")