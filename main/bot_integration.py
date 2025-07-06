import logging
from telegram import Bot
from django.conf import settings

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
CHAT_ID = settings.TELEGRAM_CHAT_ID

def send_order_to_telegram(order):
    try:
        text = (
            f"📦 Новый заказ!\n"
            f"Букет: {order.bouquet.name}\n"
            f"Цена: {order.bouquet.price} ₽\n"
            f"Дата доставки: {order.delivery_datetime.strftime('%d.%m.%Y %H:%M')}\n"
            f"Адрес: {order.delivery_address}\n"
            f"Комментарий: {order.comment or '—'}"
        )
        bot.send_message(chat_id=CHAT_ID, text=text)
        if order.bouquet.image:
            photo_url = order.bouquet.image.url
            bot.send_photo(chat_id=CHAT_ID, photo=photo_url)
        logging.info(f"Заказ #{order.pk} отправлен в Telegram.")
    except Exception as e:
        logging.error(f"Ошибка отправки заказа в Telegram: {e}")
