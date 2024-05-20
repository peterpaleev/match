# Telegram Bot for Job Applications

This Telegram bot helps users respond to job postings by generating custom cover letters and CVs.

## Features

- Upload and convert PDF resumes.
- Generate tailored responses to job descriptions.

## Setup

1. Clone the repository.
2. Create a `.env` file based on the `.env.sample`.
3. Set the `TELEGRAM_TOKEN` and `GOOGLE_APPLICATION_CREDENTIALS` appropriately.

## Deployment

Run the bot using Docker:
```bash
docker build -t telegram-bot .
docker run -p 8080:8080 telegram-bot
