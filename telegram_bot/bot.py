# telegram_bot/bot.py

import logging
from telegram import Bot
from django.conf import settings

logger = logging.getLogger(__name__)

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

def send_order_notification(order):
    """
    Отправляет в чат магазина сообщение с данными заказа.
    order - объект модели Order с полями:
      bouquet (связанный с объектом Bouquet)
      price
      delivery_date
      delivery_time
      delivery_address
      comment
    """
    try:
        bouquet = order.bouquet
        text = (
            f"🌸 *Новый заказ*\n"
            f"Букет: {bouquet.name}\n"
            f"Цена: {order.price} руб.\n"
            f"Дата и время доставки: {order.delivery_date} {order.delivery_time}\n"
            f"Адрес доставки: {order.delivery_address}\n"
        )
        if order.comment:
            text += f"Комментарий: {order.comment}\n"

        # Отправим фото букета, если есть
        if bouquet.image and bouquet.image.url:
            bot.send_photo(
                chat_id=settings.TELEGRAM_CHAT_ID,
                photo=bouquet.image.url,
                caption=text,
                parse_mode="Markdown"
            )
        else:
            # Если фото нет — просто текст
            bot.send_message(
                chat_id=settings.TELEGRAM_CHAT_ID,
                text=text,
                parse_mode="Markdown"
            )
        logger.info(f"Заказ #{order.id} отправлен в Telegram")
    except Exception as e:
        logger.error(f"Ошибка при отправке заказа #{order.id} в Telegram: {e}")
