from telegram.ext import ApplicationBuilder, CommandHandler
import logging
import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flower_project.settings")
django.setup()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update, context):
    logging.info(f"Команда /start от {update.effective_user.id}")
    await update.message.reply_text("Бот запущен и готов к работе!")

def main():
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    logging.info("Запуск бота...")
    app.run_polling()

if __name__ == "__main__":
    main()
