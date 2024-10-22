FROM python:3.11-slim

# Install dependencies for building scikit-learn
RUN apt-get update && apt-get install -y build-essential python3-dev libatlas-base-dev

# Set the working directory
WORKDIR /usr/app

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy my application code
COPY . .

# Command to run my application
CMD ["python", "flask_app_same.py"]
