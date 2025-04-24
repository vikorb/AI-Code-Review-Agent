.PHONY: help install test lint review-example streamlit clean

# Default target executed when no arguments are given to make.
help:
	@echo "Available commands:"
	@echo "  install         Install the code review agent and its dependencies"
	@echo "  test            Run unit tests"
	@echo "  lint            Run linter (flake8) on the code"
	@echo "  review-example  Run a review on the example buggy script"
	@echo "  streamlit       Run the Streamlit web interface"
	@echo "  clean           Remove build files and directories"

# Install the package and its dependencies
install:
	python -m pip install -e .

# Run tests
test:
	python run_tests.py

# Run linter
lint:
	python -m pip install flake8
	flake8 agent/ cli.py streamlit_app.py

# Run a review on the example buggy script
review-example:
	python cli.py --file examples/buggy_script.py --mode strict --provider openai

# Run the Streamlit web interface
streamlit:
	streamlit run streamlit_app.py

# Clean build files
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete