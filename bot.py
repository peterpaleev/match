from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler, CallbackQueryHandler
import os
from llm_api import process_message
from dotenv import load_dotenv
from telegram import Document
import os


load_dotenv()

# Define states for conversation
CHOOSE_ACTION, AWAIT_CV, AWAIT_JOB_DESC, PROCESS_INFO = range(4)

# User profile dictionary
user_profiles = {}

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Прислать резюме текстом", callback_data='send_cv')],
        [InlineKeyboardButton("Создать резюме (пока не доступно)", callback_data='create_cv')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Я помогу тебе быстро откликаться на вакансии ✨. Давай познакомимся, пришли свое резюме, если есть', reply_markup=reply_markup)
    return CHOOSE_ACTION

async def handle_action(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'create_cv':
        await query.message.reply_text('Создание резюме пока в разработке, но мы записали, что вам это нужно!')
        return ConversationHandler.END
    elif query.data == 'send_cv':
        await query.message.reply_text('Просто скопируй текст резюме и приши сюда')
        return AWAIT_CV

async def receive_cv(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if update.message.document:
        # If the message contains a document
        document = update.message.document
        file = await document.get_file()
        
        # Create a directory for the user if it doesn't exist
        user_directory = f"user_{user_id}"
        os.makedirs(user_directory, exist_ok=True)
        
        # Generate a unique file name
        file_name = f"cv_{user_id}_{document.file_name}"
        
        # Download and save the document
        file_path = os.path.join(user_directory, file_name)
        file.download(file_path)
        
        # Store the file path in user_profiles
        user_profiles[user_id] = {'cv': file_path}
        
        response_text = "PDF резюме получено! Теперь, пожалуйста, пришли текстом описание вакансии."
    else:
        # If the message contains text instead of a document
        document = update.message.text
        user_profiles[user_id] = {'cv': document}
        response_text = "Текстовое резюме получено! Теперь, пожалуйста, пришли описание вакансии."

    await update.message.reply_text(response_text)
    return AWAIT_JOB_DESC

async def receive_job_description(update: Update, context: CallbackContext):
    job_description = update.message.text
    user_id = update.message.from_user.id
    user_profiles[user_id]['job_description'] = job_description
    await update.message.reply_text('Job description received. Generating your custom cover letter and CV...')
    
    prompt_generate_cover_letter = "Ты бот для помощи создания сопроводительных писем и резюме под ваканию. Дальше идет резюме пользователя и описание вакансии. Создай сопроводительное письмо, отредактируй резюме. Резюме выделено --, описание вакансии выделено ++. Придумай вопросы, чтобы раскрыть кандидата и составить письмо. Вопросы выдели ^^, они должны идти после Основого ответа."

    cv_job_desc = prompt_generate_cover_letter + "--" + user_profiles[user_id]['cv'] + ' -- ++ ' + job_description + " ++"
    response_text = await process_message(cv_job_desc)

    parsed_message = response_text.split('^^')[0]

    await update.message.reply_text(parsed_message)
    return ConversationHandler.END

async def unexpected_text_handler(update: Update, context: CallbackContext):
    await update.message.reply_text("Нажми продолжить без резюме, чтобы прислать его в тексовом виде 'Продолжить без резюме'.")
    return CHOOSE_ACTION

def main():
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        raise ValueError("No token provided. Please set the TELEGRAM_TOKEN environment variable.")

    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSE_ACTION: [CallbackQueryHandler(handle_action), MessageHandler(filters.TEXT & ~filters.COMMAND, unexpected_text_handler)],
            AWAIT_CV: [MessageHandler(filters.TEXT & ~filters.ATTACHMENT, receive_cv)],
            AWAIT_JOB_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_job_description)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
