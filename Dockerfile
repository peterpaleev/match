            # FROM python:3.8-slim

            # WORKDIR /usr/src/app  
            # COPY . .  
            # RUN mkdir ./images 
            # EXPOSE 8080 
            # # Copy credentials file into the Docker image
            # COPY ps2server-maaatch-106da1f4fb1e.json /maaatch-106da1f4fb1e-322e80af70fc.json
            # # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
            # ENV GOOGLE_APPLICATION_CREDENTIALS /maaatch-106da1f4fb1e.json

            # # RUN pip install --no-cache-dir -r requirements.txt 
            # RUN pip install python-telegram-bot 
            # RUN pip install google-cloud-storage
            # RUN pip install --upgrade google-cloud-aiplatform
            # # RUN pip install google-auth
            # RUN pip install python-dotenv
            # # peterpaleev@Peters-Laptop match % docker build -t gcr.io/ps2server/telegram-bot . 
            # # peterpaleev@Peters-Laptop match % docker push gcr.io/ps2server/telegram-bot                                       
            # # RUN pip install --upgrade google-cloud-aiplatform-vertex-ai-generative-models

            # CMD ["python3", "-u", "./bot.py"]


# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run bot.py when the container launches
CMD ["python", "bot.py"]
