FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ ./app/

# Copy the main application file
COPY main.py .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "main.py"]