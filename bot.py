from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
from llm_api import process_message
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Hello! I am your cover letter assistant. Send me your resume and job description.')

async def handle_text(update: Update, context: CallbackContext):
    # Send 'I'm thinking...' message
    thinking_message = await update.message.reply_text("I'm thinking...")
    response_text = await process_message(update.message.text)
    # Edit the 'I'm thinking...' message with the actual response
    await thinking_message.edit_text(response_text)

def main():
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        raise ValueError("No token provided. Please set the TELEGRAM_TOKEN environment variable.")
    
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()

if __name__ == '__main__':
    main()
