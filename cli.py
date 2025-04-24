"""
Code Analyzer module for the Code Review Agent.

This module handles the core logic for analyzing Python code,
preparing prompts, and generating code reviews.
"""

import os
import logging
import yaml
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

from .llm_interface import LLMClient

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CodeAnalyzer:
    """Analyzes Python code and generates reviews using LLMs."""
    
    def __init__(self, provider: str, model: str, mode: str = "default", config_path: str = None):
        """
        Initialize the Code Analyzer.
        
        Args:
            provider: LLM provider to use ('openai', 'anthropic', 'ollama')
            model: The model to use
            mode: Review mode from templates (default, strict, mentor, test_focus)
            config_path: Path to config file
        """
        self.provider = provider
        self.model = model
        self.mode = mode
        self.config_path = config_path
        
        # Initialize LLM client
        self.llm_client = LLMClient(provider, model, config_path)
        
        # Load prompt templates
        self.templates = self._load_templates()
        
        if mode not in self.templates:
            logger.warning(f"Mode '{mode}' not found in templates. Using 'default'.")
            self.mode = "default"
    
    def _load_templates(self) -> Dict[str, Dict[str, str]]:
        """Load prompt templates from the templates file."""
        template_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "prompts", 
            "templates.yaml"
        )
        
        try:
            with open(template_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Templates file not found at {template_path}")
            # Provide a minimal default template
            return {
                "default": {
                    "description": "Default code review",
                    "system_prompt": "You are a Python code reviewer. Analyze the provided code for bugs, style issues, and improvements."
                }
            }
    
    def analyze_file(self, file_path: str) -> str:
        """
        Analyze a Python file and generate a review.
        
        Args:
            file_path: Path to the Python file to analyze
            
        Returns:
            A markdown-formatted code review
        """
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}"
        
        if not file_path.endswith(".py"):
            return f"Error: Only Python (.py) files are supported. Got {file_path}"
        
        try:
            with open(file_path, "r") as f:
                code_content = f.read()
            
            # Get file metadata
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            line_count = len(code_content.splitlines())
            
            logger.info(f"Analyzing {file_name} ({line_count} lines, {file_size} bytes)")
            
            # Run the review
            return self._review_code(file_name, code_content)
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return f"Error analyzing file: {str(e)}"
    
    def analyze_multiple_files(self, file_paths: List[str]) -> Dict[str, str]:
        """
        Analyze multiple Python files and generate reviews for each.
        
        Args:
            file_paths: List of paths to Python files
            
        Returns:
            Dictionary mapping file paths to reviews
        """
        results = {}
        for file_path in file_paths:
            results[file_path] = self.analyze_file(file_path)
        return results
    
    def _review_code(self, file_name: str, code_content: str) -> str:
        """
        Generate a code review for the provided code.
        
        Args:
            file_name: Name of the file being reviewed
            code_content: Python code to review
            
        Returns:
            Markdown-formatted code review
        """
        # Get the appropriate prompt template
        template = self.templates[self.mode]
        system_prompt = template["system_prompt"]
        
        # Construct the user prompt with context
        user_prompt = f"Please review the following Python code from file '{file_name}'."
        
        # Check if the code is too long
        if len(code_content) > 15000:  # Arbitrary limit to avoid token limits
            logger.warning(f"Code is very long ({len(code_content)} chars). Truncating.")
            code_content = code_content[:15000] + "\n# ... [truncated due to length]"
        
        # Call the LLM to generate the review
        logger.info(f"Sending code to {self.provider} using mode: {self.mode}")
        start_time = time.time()
        
        review = self.llm_client.run(system_prompt, user_prompt, code_content)
        
        elapsed_time = time.time() - start_time
        logger.info(f"Review generated in {elapsed_time:.2f} seconds")
        
        # Add metadata header
        metadata = (
            f"# Code Review: {file_name}\n\n"
            f"* **File:** {file_name}\n"
            f"* **Review Mode:** {self.mode}\n"
            f"* **Provider:** {self.provider}\n"
            f"* **Model:** {self.model}\n"
            f"* **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"---\n\n"
        )
        
        return metadata + review
    
    def save_review(self, review: str, file_path: str, output_dir: Optional[str] = None) -> str:
        """
        Save a review to a markdown file.
        
        Args:
            review: The review content
            file_path: Path to the original file (used to generate the output name)
            output_dir: Directory to save the review (defaults to ./reviews)
            
        Returns:
            Path to the saved review file
        """
        if not output_dir:
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reviews")
        
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate a filename based on the original file
        base_name = os.path.basename(file_path)
        file_name, _ = os.path.splitext(base_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        review_file = f"{file_name}_review_{timestamp}.md"
        review_path = os.path.join(output_dir, review_file)
        
        # Save the review
        with open(review_path, "w") as f:
            f.write(review)
        
        logger.info(f"Review saved to {review_path}")
        return review_path


# For testing purposes
if __name__ == "__main__":
    # Sample test
    try:
        analyzer = CodeAnalyzer("openai", "gpt-4", "default")
        # Replace with a path to a real Python file
        sample_file = "../examples/buggy_script.py"
        if os.path.exists(sample_file):
            review = analyzer.analyze_file(sample_file)
            print(review)
    except Exception as e:
        logger.error(f"Test failed: {e}")