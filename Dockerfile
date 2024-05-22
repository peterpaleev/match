# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Explicitly copy the requirements.txt first
COPY requirements.txt ./

# Check that requirements.txt is copied
RUN ls -l 

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the remaining directory contents into the container at /app
COPY . /app

# Copy the Google Cloud service account key file into the container
COPY maaatch-106da1f4fb1e.json /usr/src/app/service-account-file.json

# Set the Google Application Credentials environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/src/app/service-account-file.json


# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run bot.py when the container launches
CMD ["python", "bot.py"]
