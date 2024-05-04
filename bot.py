from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os
from llm_api import process_message
from dotenv import load_dotenv

from telegram import Update
from telegram.constants import ParseMode

# Load environment variables from .env file
load_dotenv()

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Hello! I am your cover letter assistant. Send me your resume and job description.')

async def handle_text(update: Update, context: CallbackContext):
    # Send 'I'm thinking...' message
    thinking_message = await update.message.reply_text("I'm thinking...")

    pre_prompt = "Ты бот для составления резюме Match. Пользователь должен прислать описание вакансии. Составь сопроводительное письмо и задай вопросы пользоватею об его опытеб чтобы дополнить резюме. Если пользователь не прислал вакансю, потребуй это! Затем предложи прислать резюме, чтобы скорректировать его. после -- идет ответ пользователя. Каждый вопрос выдели ++ с двух сторон. Цель - составить резюме под вакансию на основе изначального резюме --"
    
    cv_example = "-- резюме пользователя -- # Петр Палеев ![IMG_1308.JPG](https://prod-files-secure.s3.us-west-2.amazonaws.com/0f9b0748-f6c8-46c4-bdd3-fa4755961076/6bcf801f-2ede-4e4f-b685-1a8ce116cf9d/IMG_1308.jpg) ## Общая информация - Город: Москва - Телефон: +7 (929) 926-80-40 - Email: [petpal005@gmail.com](mailto:petpal005@gmail.com) ## Опыт работы ### Windy.app (2020 - Настоящее время) - **Full-stack инженер(april 2020- feb 2023)**: - **Инженер Full-stack**: май 2020 - февраль 2023 Использование Python, JavaScript, SQL, HTML, CSS, PHP, Clickhouse и др. - **Руководитель инженерной группы (член команды по росту)**: маркетинговые воронки с сайта на сайт Включал в себя разработку новой логики подписок, вопросы оплаты и налогообложения. Развитие на основе данных. Исследование пользовательского опыта. Маркетинговая аналитика. Сотрудничество команд веб-разработки и бэкенда. [windy.app/w2w](http://windy.app/w2w) февраль 2023 - ноябрь 2023 - **Продуктовый менеджер (конкурс экспериментальных функций)**: стикер для обмена Экспериментальный продукт, предназначенный для деления в социальных сетях, моя роль - мини-основатель, сосредоточенный на исследовании пользовательских потоков и общей разработке. [windy.app/sticker](http://windy.app/sticker) ноябрь 2023 - **Аналитик продукта** (для адаптации, общей аналитики продукта, веб-аналитики) Различные информационные панели для разных приложений. Использование Amplitude, Clickhouse, Redash, Cosmograph, SQL - Работа над улучшением пользовательского опыта - Сотрудничество с командами разработки и маркетинга ## Образование ### МИСИС - Специальность: Физика 3.0.0 - Годы обучения: 2018 - 2022 Python, Статистика, Мат анализ ### ВШЭ - Специальность: Дизайн - Годы обучения: 2020 - 2022 Курс Вадима Булгакова по дизайну и программированию [Проект приложения для хранения вещей](https://www.notion.so/d248e224efa8487f903a936340349e04?pvs=21)"
    
    # Process the message
    response_text = await process_message(pre_prompt + update.message.text + cv_example)
    
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
