# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the app and install dependencies
COPY . /app
RUN pip install -r requirements.txt

# Expose the port and define the start command
EXPOSE 8080
CMD ["python", "app.py"]
