FROM python:3.10-slim AS base

# Avoid Python buffering and set working dir
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# system dependencies (needed for MySQL client & pandas)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first 
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the application code
COPY . .

# Streamlit uses this port
EXPOSE 8501

# Default Streamlit command
CMD ["streamlit", "run", "streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
