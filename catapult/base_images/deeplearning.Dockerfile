# Use NVIDIA's PyTorch image as a base (includes CUDA support)
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

# Set the working directory
WORKDIR /app

# Install additional system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["python", "train.py"]