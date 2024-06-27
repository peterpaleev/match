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

# Install aiohttp
RUN pip install aiohttp

# Copy the remaining directory contents into the container at /app
COPY . /app

# Copy the Google Cloud service account key file into the container
COPY maaatch-106da1f4fb1e.json /usr/src/app/service-account-file.json

# Set the Google Application Credentials environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/src/app/service-account-file.json

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Copy supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set environment variables for database connection
ENV DATABASE_URL=postgresql+psycopg2://username:password@hostname:port/dbname

# Run supervisord
CMD ["python", "bot.py"]
