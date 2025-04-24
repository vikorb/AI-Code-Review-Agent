FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Compile Python files
RUN python -m compileall .

# Install the package
RUN pip install -e .

# Expose port for Streamlit
EXPOSE 8501

# Command to run
ENTRYPOINT ["python"]
CMD ["cli.py", "--help"]

# To run the Streamlit app instead, use:
# CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]