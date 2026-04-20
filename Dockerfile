FROM python:3.12-slim

WORKDIR /app

# Install system essentials
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Fix Windows line endings in the shell script and make it executable
RUN sed -i 's/\r$//' start.sh
RUN chmod +x start.sh

# Expose ports
EXPOSE 8000
EXPOSE 7860

# Use the shell form of CMD to ensure start.sh runs correctly
CMD ["/bin/bash", "./start.sh"]