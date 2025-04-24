# 🔍 AI Code Review Agent

An AI-powered code review tool that analyzes Python code and provides detailed feedback on bugs, style issues, and potential improvements. Works with OpenAI, Anthropic Claude, or local Ollama models.

## 🌟 Features

- **Dual-Mode Operation**: Use either commercial AI APIs (OpenAI, Anthropic) or local models (Ollama)
- **Multiple Review Styles**: Choose from different review personalities and focus areas
- **Detailed Analysis**: Identifies bugs, style issues, improvement suggestions, and more
- **Markdown Reports**: Generate well-formatted code review reports
- **File & Batch Processing**: Review single files or multiple files at once
- **Customizable**: Configure via YAML config and command-line options

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/code-review-agent.git
   cd code-review-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API keys (for OpenAI or Anthropic):
   - Edit `config.yaml` and add your API keys, or
   - Set environment variables:
     ```bash
     export OPENAI_API_KEY="your_openai_key"
     export ANTHROPIC_API_KEY="your_anthropic_key"
     ```

## 🚀 Usage

### Command Line Interface

Basic usage:

```bash
python cli.py --file path/to/your/python_file.py
```

With more options:

```bash
python cli.py --file path/to/your/python_file.py --mode strict --provider openai --model gpt-4
```

Review multiple files:

```bash
python cli.py --file file1.py --file file2.py --file file3.py
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--file`, `-f` | Path to Python file(s) to analyze | Required |
| `--mode`, `-m` | Review mode to use | `default` |
| `--provider`, `-p` | LLM provider (`openai`, `anthropic`, `ollama`) | `openai` |
| `--model`, `-M` | Specific model to use | Provider's default |
| `--config`, `-c` | Path to config file | `./config.yaml` |
| `--output-dir`, `-o` | Directory to save reviews | `./reviews` |
| `--verbose`, `-v` | Enable verbose output | `False` |

### Review Modes

The agent supports several review modes, each with a different focus:

- `default`: Balanced review focusing on bugs, code quality, and improvements
- `strict`: Meticulous review focusing on best practices and standards
- `mentor`: Educational review with constructive feedback for learning
- `test_focus`: Review focused on testing and test coverage
- `security`: Review focused on security vulnerabilities and issues

## ⚙️ Configuration

You can customize the agent through the `config.yaml` file:

```yaml
# API Keys
api_keys:
  openai: "YOUR_OPENAI_API_KEY"
  anthropic: "YOUR_ANTHROPIC_API_KEY"

# Default models
models:
  openai: "gpt-4"
  anthropic: "claude-3-sonnet-20240229"
  ollama: "mistral"

# Default review mode
default_mode: "default"

# Output settings
output:
  directory: "reviews"
  format: "markdown"
```

## 📁 Project Structure

```
code_review_agent/
├── agent/
│   ├── analyzer.py          # Review logic + prompt construction
│   └── llm_interface.py     # Unified API/Ollama abstraction
├── examples/
│   ├── buggy_script.py      # Example with intentional issues
│   └── clean_script.py      # Example with best practices
├── prompts/
│   └── templates.yaml       # Stores different prompt styles
├── reviews/
│   └── .gitkeep             # Output directory for reviews
├── cli.py                   # Command-line runner
├── config.yaml              # API keys, model config
├── README.md                # This file
└── requirements.txt         # Dependencies
```

## 🔄 Adding Custom Review Modes

You can add your own review modes by editing `prompts/templates.yaml`:

```yaml
your_mode_name:
  description: "Description of your review mode"
  system_prompt: |
    Custom system prompt for the LLM that defines how to review the code...
```

## 🧪 Example Reviews

Try running the agent on the included example files:

```bash
python cli.py --file examples/buggy_script.py --mode strict
```

Or with a different review mode:

```bash
python cli.py --file examples/clean_script.py --mode mentor
```

## 🔧 Development

To extend the agent or modify its behavior:

- Add new LLM providers by extending the `LLMClient` class in `llm_interface.py`
- Add new analysis features in the `CodeAnalyzer` class in `analyzer.py`
- Create custom review modes in `prompts/templates.yaml`

## 📄 License

MIT License

## 📝 Note on AI Providers

- **OpenAI**: Requires an API key and charges based on token usage
- **Anthropic**: Requires an API key and charges based on token usage
- **Ollama**: Free, runs locally, but requires the Ollama application to be installed and running

## 💡 Future Enhancements

- Web UI with Streamlit
- Support for languages other than Python
- Interactive reviews with suggestion application
- Integration with git workflows
- Custom rules and linting integration