from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import asyncio
from llm_api import process_message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am your cover letter assistant. Send me your resume and job description.')

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    port = int(os.getenv('PORT', '8080'))
    application.run_polling(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
