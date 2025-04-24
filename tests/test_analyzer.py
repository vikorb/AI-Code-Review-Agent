"""
Unit tests for the CodeAnalyzer class.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.analyzer import CodeAnalyzer


class TestCodeAnalyzer(unittest.TestCase):
    """Tests for the CodeAnalyzer class."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock the LLMClient to avoid API calls during tests
        self.llm_patcher = patch('agent.analyzer.LLMClient')
        self.mock_llm = self.llm_patcher.start()
        
        # Create a mock response for the LLM
        self.mock_llm.return_value.run.return_value = "# Mock Review\n\nThis is a mock review."
        
        # Create a test analyzer
        self.analyzer = CodeAnalyzer("mock", "mock-model", "default")
    
    def tearDown(self):
        """Tear down test environment."""
        self.llm_patcher.stop()
    
    def test_init(self):
        """Test CodeAnalyzer initialization."""
        self.assertEqual(self.analyzer.provider, "mock")
        self.assertEqual(self.analyzer.model, "mock-model")
        self.assertEqual(self.analyzer.mode, "default")
        
        # Test with invalid mode
        analyzer = CodeAnalyzer("mock", "mock-model", "nonexistent_mode")
        self.assertEqual(analyzer.mode, "default")  # Should default to "default"
    
    def test_load_templates(self):
        """Test loading prompt templates."""
        templates = self.analyzer._load_templates()
        
        # Check that we have at least the default template
        self.assertIn("default", templates)
        self.assertIn("system_prompt", templates["default"])
    
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, 
           read_data="def test():\n    return True")
    def test_analyze_file(self, mock_open, mock_exists):
        """Test analyzing a Python file."""
        # Set up mocks
        mock_exists.return_value = True
        
        # Test file analysis
        result = self.analyzer.analyze_file("test.py")
        
        # Verify file was checked and opened
        mock_exists.assert_called_once_with("test.py")
        mock_open.assert_called_once_with("test.py", "r")
        
        # Check that the result includes our mock review
        self.assertIn("Mock Review", result)
        
        # Check that metadata was added
        self.assertIn("# Code Review: test.py", result)
        self.assertIn("Review Mode:", result)
        self.assertIn("Provider:", result)
    
    @patch('os.path.exists')
    def test_analyze_nonexistent_file(self, mock_exists):
        """Test analyzing a file that doesn't exist."""
        # Set up mock
        mock_exists.return_value = False
        
        # Test nonexistent file
        result = self.analyzer.analyze_file("nonexistent.py")
        
        # Verify error message
        self.assertIn("Error: File not found", result)
    
    def test_analyze_non_python_file(self):
        """Test analyzing a non-Python file."""
        # Test non-Python file
        result = self.analyzer.analyze_file("test.txt")
        
        # Verify error message
        self.assertIn("Error: Only Python (.py) files are supported", result)
    
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_review(self, mock_open, mock_makedirs):
        """Test saving a review to a file."""
        # Test saving review
        review = "# Test Review\n\nThis is a test review."
        result = self.analyzer.save_review(review, "test.py", "test_output")
        
        # Verify directory was created
        mock_makedirs.assert_called_once_with("test_output", exist_ok=True)
        
        # Verify file was opened for writing
        mock_open.assert_called_once()
        self.assertTrue(mock_open.call_args[0][0].endswith(".md"))
        
        # Verify review was written
        mock_open().write.assert_called_once_with(review)
        
        # Verify result is the path
        self.assertTrue(result.endswith(".md"))


if __name__ == '__main__':
    unittest.main()