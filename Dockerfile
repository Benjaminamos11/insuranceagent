FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for Swiss Insurance Agent
RUN pip install --no-cache-dir \
    nest_asyncio \
    webcolors \
    GitPython \
    supabase \
    stripe \
    python-multipart

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p work_dir logs templates assets config

# Set permissions
RUN chmod +x run_ui.py

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Environment variables
ENV PYTHONPATH=/app
ENV WEB_UI_PORT=8080
ENV WEB_UI_HOST=0.0.0.0

# Start application
CMD ["python3", "run_ui.py", "--host", "0.0.0.0", "--port", "8080"] 