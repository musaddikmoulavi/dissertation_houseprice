FROM python:3.12-slim

# Install system dependencies and Rust
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    g++ \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && . $HOME/.cargo/env \
    && rustc --version \
    && cargo --version \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install Cython==3.0.0 && pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the application port (optional, based on your app)
EXPOSE 8000

# Command to run the application
CMD ["python", "server.py"]
