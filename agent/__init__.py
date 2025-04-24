"""
AI Code Review Agent package.

This package provides components for analyzing Python code
and generating reviews using large language models.
"""

__version__ = "0.1.0"

from .analyzer import CodeAnalyzer
from .llm_interface import LLMClient

__all__ = ["CodeAnalyzer", "LLMClient"]