# Use the official Python image from the Docker Hub
FROM python:3.12.3-slim

# Set the working directory in the container
WORKDIR /app

RUN mkdir instance

# Copy the requirements file into the container
COPY requirements.txt .

RUN pip install --upgrade pip

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 1111 for the Flask app
EXPOSE 1111

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=1111"]
