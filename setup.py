#!/usr/bin/env python3
"""
Setup script for the AI Code Review Agent package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="code_review_agent",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered code review agent for Python files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code-review-agent",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "code-review=code_review_agent.cli:main",
        ],
    },
)