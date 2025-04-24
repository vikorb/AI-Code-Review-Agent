# Installation Guide for AI Code Review Agent

This guide explains how to install and set up the AI Code Review Agent on your system.

## Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Git
- API keys for OpenAI or Anthropic (if using those providers)
- Ollama installed locally (if using Ollama provider)

## Installation Methods

### Method 1: Quick Installation

The fastest way to install is directly from GitHub:

```bash
# Clone the repository
git clone https://github.com/yourusername/code-review-agent.git
cd code-review-agent

# Install the package and dependencies
pip install -e .
```

### Method 2: Manual Installation

If you prefer to manually install:

```bash
# Clone the repository
git clone https://github.com/yourusername/code-review-agent.git
cd code-review-agent

# Install dependencies
pip install -r requirements.txt
```

### Method 3: Docker Installation

If you prefer to use Docker:

```bash
# Clone the repository
git clone https://github.com/yourusername/code-review-agent.git
cd code-review-agent

# Build and run the Docker image
docker-compose build
```

## Configuration

### API Keys

You have two options for configuring API keys:

#### Option 1: Environment Variables

Set the following environment variables:

```bash
# For OpenAI
export OPENAI_API_KEY="your_openai_api_key"

# For Anthropic
export ANTHROPIC_API_KEY="your_anthropic_api_key"
```

#### Option 2: Config File

Edit the `config.yaml` file in the project root:

```yaml
api_keys:
  openai: "YOUR_OPENAI_API_KEY"
  anthropic: "YOUR_ANTHROPIC_API_KEY"
```

### Using Ollama

If you want to use Ollama (local models):

1. Install Ollama from [https://ollama.ai/](https://ollama.ai/)
2. Start the Ollama service
3. Pull the models you want to use:
   ```bash
   ollama pull mistral
   ollama pull codellama
   ```

## Verifying Installation

To verify that everything is working correctly:

```bash
# Run the tests
python run_tests.py

# Try running a code review on an example file
python cli.py --file examples/buggy_script.py --mode default --provider openai
```

## Running the Web Interface

To use the Streamlit web interface:

```bash
streamlit run streamlit_app.py
```

Or with Docker:

```bash
docker-compose up code-review-web
```

Then open your browser to http://localhost:8501

## Troubleshooting

### Common Issues

1. **API Key Errors**: Make sure your API keys are correctly set in either the config file or environment variables.

2. **Module Not Found Errors**: Make sure you've installed the package or all its dependencies correctly.

3. **Ollama Connection Issues**: Check that the Ollama service is running on port 11434.

4. **Permission Issues**: If you see permission errors when saving reviews, check that the reviews directory exists and is writable.

### Getting Help

If you encounter any issues not covered here, please:

1. Check the existing issues on the GitHub repository
2. Create a new issue with a detailed description of your problem

## Uninstallation

To uninstall the package:

```bash
pip uninstall code-review-agent
```

To completely remove all files:

```bash
# Remove the repository directory
rm -rf /path/to/code-review-agent
```