from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler, CallbackQueryHandler
import os
from llm_api import process_message, process_pdf_file
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

load_dotenv()

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL')
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define database models
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Resume(Base):
    __tablename__ = 'resumes'
    resume_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    resume_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user = relationship("User", back_populates="resumes")

class JobDescription(Base):
    __tablename__ = 'job_descriptions'
    job_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    job_description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="job_descriptions")

class CoverLetter(Base):
    __tablename__ = 'cover_letters'
    cover_letter_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    job_id = Column(Integer, ForeignKey('job_descriptions.job_id'))
    cover_letter_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="cover_letters")
    job = relationship("JobDescription", back_populates="cover_letters")

class UserResponse(Base):
    __tablename__ = 'user_responses'
    response_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="responses")

class Template(Base):
    __tablename__ = 'templates'
    template_id = Column(Integer, primary_key=True)
    template_name = Column(String)
    template_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

User.resumes = relationship("Resume", order_by=Resume.resume_id, back_populates="user")
User.job_descriptions = relationship("JobDescription", order_by=JobDescription.job_id, back_populates="user")
User.cover_letters = relationship("CoverLetter", order_by=CoverLetter.cover_letter_id, back_populates="user")
User.responses = relationship("UserResponse", order_by=UserResponse.response_id, back_populates="user")

# Create tables
Base.metadata.create_all(engine)

# Telegram bot states
CHOOSE_ACTION, AWAIT_CV, AWAIT_JOB_DESC, PROCESS_INFO = range(4)

# User profile dictionary
user_profiles = {}

async def start(update: Update, context: CallbackContext):
    print("Command /start received")
    keyboard = [
        [InlineKeyboardButton("Прислать резюме", callback_data='send_cv')],
        [InlineKeyboardButton("Создать резюме (пока не доступно)", callback_data='create_cv')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Я помогу тебе быстро откликаться на вакансии ✨. Давай познакомимся, пришли свое резюме, если есть', reply_markup=reply_markup)
    return CHOOSE_ACTION

async def handle_action(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    username = query.from_user.username

    # Check if user exists, if not create a new user
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        user = User(user_id=user_id, username=username)
        session.add(user)
        session.commit()

    print(f"User {user_id} selected action: {query.data}")

    if query.data == 'create_cv':
        await query.message.reply_text('Создание резюме пока в разработке, но мы записали, что вам это нужно!')
        return ConversationHandler.END
    elif query.data == 'send_cv':
        await query.message.reply_text('Пришли файл или просто текст')
        return AWAIT_CV

async def receive_cv(update, context):
    user_id = update.message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()
    print(f"Received resume from user {user_id}")

    if update.message.document:
        document = update.message.document
        file = await document.get_file()

        user_directory = f"user_{user_id}"
        os.makedirs(user_directory, exist_ok=True)
        file_path = os.path.join(user_directory, document.file_name)

        await file.download_to_drive(file_path)  # Async download call

        print(f"Downloaded file to {file_path}")
        converted_text = await process_pdf_file(user_id, file_path)
        print(converted_text)

        # Save resume to database
        resume = Resume(user_id=user_id, resume_data={'text': converted_text})
        session.add(resume)
        session.commit()

        response_text = "Резюме получено! Теперь отправь текст вакансии"
    else:
        resume_text = update.message.text

        # Save resume to database
        resume = Resume(user_id=user_id, resume_data={'text': resume_text})
        session.add(resume)
        session.commit()

        response_text = "Резюме получено! Теперь отправь текст вакансии."

    await update.message.reply_text(response_text)
    return AWAIT_JOB_DESC

async def receive_job_description(update: Update, context: CallbackContext):
    job_description_text = update.message.text
    user_id = update.message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()

    # Save job description to database
    job_description = JobDescription(user_id=user_id, job_description=job_description_text)
    session.add(job_description)
    session.commit()

    print(f"Job description received from user {user_id}")

    await update.message.reply_text('Job description received. Generating your custom cover letter and CV...')
    prompt_generate_cover_letter = "Ты бот для помощи создания сопроводительных писем и резюме под ваканию. Дальше идет резюме пользователя и описание вакансии. Создай сопроводительное письмо, отредактируй резюме. Резюме выделено --, описание вакансии выделено ++. Придумай вопросы, чтобы раскрыть кандидата и составить письмо. Вопросы выдели ^^, они должны идти после Основого ответа."

    response_text = await process_message(
        prompt_generate_cover_letter +
        " -- " + 
        user_profiles[user_id]['cv'] + 
        " -- ++" + 
        job_description_text + 
        "++"
        )
    
    response_text = escape_markdown(response_text)

    # Save cover letter to database
    cover_letter = CoverLetter(user_id=user_id, job_id=job_description.job_id, cover_letter_data={'text': response_text})
    session.add(cover_letter)
    session.commit()

    await update.message.reply_text(response_text, parse_mode='Markdown')    
    return ConversationHandler.END

def escape_markdown(text):
    markdown_chars = ['*', '_', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in markdown_chars:
        text = text.replace(char, '\\' + char)
    return text

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
            AWAIT_CV: [MessageHandler(filters.ATTACHMENT | filters.TEXT, receive_cv)],
            AWAIT_JOB_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_job_description)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
