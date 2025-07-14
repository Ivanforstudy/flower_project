# файл: main/telegram_utils.py

import logging
import requests
from django.conf import settings

# Замените на свои значения или импортируйте из настроек
BOT_TOKEN = "7763598812:AAHa-yOc3rZ0wINeAptiE6ktRflzADi_OqU"
CHAT_ID = '2111297101'

def send_order_to_telegram(order):
    try:
        order_items = order.items.all()
        bouquets_info = []

        for item in order_items:
            bouquets_info.append(f"{item.quantity}x {item.bouquet.name}")

        bouquets_text = ", ".join(bouquets_info)

        text = (
            f"📦 Новый заказ!\n"
            f"Букеты: {bouquets_text}\n"
            f"Общая цена: {order.total_price} ₽\n"
            f"Дата доставки: {order.delivery_datetime.strftime('%d.%m.%Y %H:%M')}\n"
            f"Адрес: {order.delivery_address}\n"
            f"Комментарий: {order.comment or '—'}"
        )

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': CHAT_ID,
            'text': text
        }
        response = requests.post(url, data=data)

        if response.status_code != 200:
            logging.error(f"Ошибка Telegram API: {response.text}")
        else:
            logging.info(f"Заказ #{order.pk} успешно отправлен в Telegram.")

    except Exception as e:
        logging.error(f"Ошибка отправки заказа в Telegram: {e}")
