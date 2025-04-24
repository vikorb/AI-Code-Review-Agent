"""
Streamlit web interface for the Code Review Agent.

Run with:
    streamlit run streamlit_app.py
"""

import os
import sys
import yaml
import tempfile
from pathlib import Path
import streamlit as st
from typing import List, Dict, Any

# Import the agent modules
from agent.analyzer import CodeAnalyzer
from agent.llm_interface import LLMClient

# Set page config
st.set_page_config(
    page_title="AI Code Review Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define paths
ROOT_DIR = Path(__file__).parent
CONFIG_PATH = ROOT_DIR / "config.yaml"
TEMPLATES_PATH = ROOT_DIR / "prompts" / "templates.yaml"


def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        st.warning(f"Config file not found at {CONFIG_PATH}. Using defaults.")
        return {}


def get_available_modes() -> List[str]:
    """Get available review modes from templates file."""
    try:
        with open(TEMPLATES_PATH, "r") as f:
            templates = yaml.safe_load(f)
        return list(templates.keys())
    except Exception as e:
        st.error(f"Error loading templates: {e}")
        return ["default"]


def get_mode_descriptions() -> Dict[str, str]:
    """Get descriptions for each review mode."""
    try:
        with open(TEMPLATES_PATH, "r") as f:
            templates = yaml.safe_load(f)
        return {mode: data.get("description", "") for mode, data in templates.items()}
    except Exception:
        return {"default": "Standard code review"}


def analyze_code(
    code: str,
    file_name: str,
    provider: str,
    model: str,
    mode: str,
    api_key: str = None,
) -> str:
    """Analyze the provided code and generate a review."""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
            temp_file.write(code.encode())
            temp_path = temp_file.name
        
        # Set the API key if provided
        if api_key:
            os.environ[f"{provider.upper()}_API_KEY"] = api_key
        
        # Initialize the analyzer
        analyzer = CodeAnalyzer(
            provider=provider,
            model=model,
            mode=mode,
        )
        
        # Generate review
        review = analyzer.analyze_file(temp_path)
        
        # Clean up
        os.unlink(temp_path)
        
        return review
    
    except Exception as e:
        return f"Error analyzing code: {str(e)}"


def main() -> None:
    """Main Streamlit app function."""
    # Load configurations
    config = load_config()
    available_modes = get_available_modes()
    mode_descriptions = get_mode_descriptions()
    
    # Header
    st.title("🔍 AI Code Review Agent")
    st.markdown(
        "Upload or paste Python code to get AI-powered code review feedback."
    )
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    
    # Provider selection
    provider = st.sidebar.radio(
        "LLM Provider",
        options=["openai", "anthropic", "ollama"],
        index=0,
        help="Select which AI provider to use for the code review",
    )
    
    # Model selection based on provider
    default_models = {
        "openai": ["gpt-4", "gpt-3.5-turbo"],
        "anthropic": ["claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
        "ollama": ["mistral", "llama2", "codellama"],
    }
    
    # Get default model from config or use the first in the list
    config_default = config.get("models", {}).get(provider)
    default_index = 0
    if config_default in default_models[provider]:
        default_index = default_models[provider].index(config_default)
    
    model = st.sidebar.selectbox(
        "Model",
        options=default_models[provider],
        index=default_index,
        help="Select which model version to use",
    )
    
    # Review mode selection
    mode = st.sidebar.selectbox(
        "Review Mode",
        options=available_modes,
        index=0,
        help="Select the style of code review",
    )
    
    # Display the description of the selected mode
    if mode in mode_descriptions:
        st.sidebar.info(mode_descriptions[mode])
    
    # API Key input
    if provider != "ollama":
        api_key = st.sidebar.text_input(
            f"{provider.capitalize()} API Key",
            type="password",
            help=f"Enter your {provider} API key (or set it in config.yaml)",
            value=config.get("api_keys", {}).get(provider, ""),
        )
    else:
        api_key = None
        st.sidebar.info(
            "Ollama requires the Ollama application to be running locally. "
            "No API key needed."
        )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Input Code")
        
        # File upload option
        uploaded_file = st.file_uploader("Upload Python file", type=["py"])
        
        if uploaded_file:
            file_name = uploaded_file.name
            code = uploaded_file.getvalue().decode("utf-8")
            st.code(code, language="python")
        else:
            file_name = "input.py"
            code = st.text_area(
                "Or paste your code here",
                height=400,
                placeholder="def hello_world():\n    print('Hello, World!')",
            )
    
    # Review button
    if st.button("Generate Review", type="primary", disabled=not code):
        with st.spinner("Analyzing code..."):
            review = analyze_code(
                code=code,
                file_name=file_name,
                provider=provider,
                model=model,
                mode=mode,
                api_key=api_key,
            )
            
            with col2:
                st.header("Code Review")
                st.markdown(review)
                
                # Add download button for the review
                st.download_button(
                    label="Download Review",
                    data=review,
                    file_name=f"{Path(file_name).stem}_review.md",
                    mime="text/markdown",
                )
    else:
        with col2:
            st.header("Code Review")
            st.info("Submit your code to generate a review")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "AI Code Review Agent | [GitHub Repository](https://github.com/yourusername/code-review-agent)"
    )


if __name__ == "__main__":
    main()