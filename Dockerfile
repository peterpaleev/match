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

RUN pip install aiohttp

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

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run supervisord
# CMD ["/usr/bin/supervisord"]

CMD ["python", "health_check_server.py"]

