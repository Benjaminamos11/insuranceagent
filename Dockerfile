FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    gcc \
    g++ \
    make \
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
RUN mkdir -p logs data memory

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=50001

# Expose port
EXPOSE 50001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:50001/health || exit 1

# Run the application
CMD ["python", "run_ui.py"] 