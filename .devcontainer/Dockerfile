# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Explicitly copy the requirements.txt first
COPY requirements.txt ./
RUN ls -l # Check that requirements.txt is copied

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the remaining directory contents into the container at /app
COPY . /app

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run bot.py when the container launches
CMD ["python", "bot.py"]
