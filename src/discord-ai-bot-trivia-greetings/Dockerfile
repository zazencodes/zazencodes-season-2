# Use the official Python image as a base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the bot
CMD ["python", "main.py"]
