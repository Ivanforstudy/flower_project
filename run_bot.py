# run_bot.py

import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Этапы разговора
NAME, IMAGE, PRICE, DATE, TIME, ADDRESS, COMMENT, CONFIRM = range(8)

# Старт команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Здравствуйте! Давайте оформим заказ. Как называется букет?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Отправьте изображение букета.")
    return IMAGE

async def get_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message.photo:
        await update.message.reply_text("Пожалуйста, отправьте изображение.")
        return IMAGE

    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    context.user_data['image_file_id'] = photo_file.file_id
    await update.message.reply_text("Укажите цену букета.")
    return PRICE

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['price'] = update.message.text
    await update.message.reply_text("Введите дату доставки (например, 2025-07-08).")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['date'] = update.message.text
    await update.message.reply_text("Введите время доставки (например, 14:00).")
    return TIME

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['time'] = update.message.text
    await update.message.reply_text("Введите адрес доставки.")
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['address'] = update.message.text
    await update.message.reply_text("Добавьте комментарий к заказу (или напишите 'нет').")
    return COMMENT

async def get_comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['comment'] = update.message.text
    data = context.user_data

    summary = (
        f"Ваш заказ:\n"
        f"Название: {data['name']}\n"
        f"Цена: {data['price']} руб\n"
        f"Дата доставки: {data['date']}\n"
        f"Время доставки: {data['time']}\n"
        f"Адрес: {data['address']}\n"
        f"Комментарий: {data['comment']}"
    )

    await update.message.reply_photo(
        photo=data['image_file_id'],
        caption=summary
    )

    await update.message.reply_text("Спасибо! Заказ принят.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Заказ отменён.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Токен бота
BOT_TOKEN = "7763598812:AAHa-yOc3rZ0wINeAptiE6ktRflzADi_OqU"

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            IMAGE: [MessageHandler(filters.PHOTO, get_image)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            COMMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_comment)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    logging.info("Бот запущен и готов к работе.")
    app.run_polling()
