# telegram_bot/bot.py

import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from main.models import Order
import django
import os
import sys

# Настройка Django окружения
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flower_project.settings")
django.setup()

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = 'YOUR_BOT_TOKEN'  # замени на свой

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌸 Добро пожаловать в Flower Delivery Bot!\nЯ покажу тебе заказы клиентов.")

async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orders = Order.objects.all().order_by('-created_at')[:5]
    if not orders:
        await update.message.reply_text("Пока нет заказов.")
        return

    for order in orders:
        flower = order.flower
        text = (
            f"🌷 Букет: {flower.name}\n"
            f"💰 Цена: {flower.price} руб.\n"
            f"📍 Адрес: {order.address}\n"
            f"📅 Доставка: {order.delivery_date} в {order.delivery_time}\n"
            f"💬 Комментарий: {order.comment or '—'}"
        )
        if flower.image:
            await update.message.reply_photo(photo=open(flower.image.path, 'rb'), caption=text)
        else:
            await update.message.reply_text(text)

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("orders", orders))
    print("Bot started...")
    app.run_polling()
