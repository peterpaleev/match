FROM python:3.10.12  
WORKDIR /usr/src/app  
COPY . .  
RUN mkdir ./images 
# Copy credentials file into the Docker image
COPY ps2server-322e80af70fc.json /ps2server-322e80af70fc.json
# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS /ps2server-322e80af70fc.json

# RUN pip install --no-cache-dir -r requirements.txt 
RUN pip install python-telegram-bot 
RUN pip install google-cloud-storage
RUN pip install --upgrade google-cloud-aiplatform
# RUN pip install google-auth
RUN pip install python-dotenv
# peterpaleev@Peters-Laptop match % docker build -t gcr.io/ps2server/telegram-bot . 
# peterpaleev@Peters-Laptop match % docker push gcr.io/ps2server/telegram-bot                                       
# RUN pip install --upgrade google-cloud-aiplatform-vertex-ai-generative-models

CMD ["python", "-u", "./bot.py"] && ["gunicorn", "-b", "0.0.0.0:$PORT", "your_application_module:app"]
