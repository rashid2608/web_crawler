# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY src/requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ /app/

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME WebCrawler

# Run server.py when the container launches
CMD ["python", "server.py"]