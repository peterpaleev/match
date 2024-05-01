FROM python:3.10.12  
WORKDIR /usr/src/app  
COPY . .  
RUN mkdir ./images 
RUN pip install --no-cache-dir -r requirements.txt 
RUN pip install python-telegram-bot
CMD ["python", "-u", "./bot.py"] 
