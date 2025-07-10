import logging
import os
import sys
import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
import django

# Django setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_project.settings')
django.setup()

from main.models import Bouquet, Order
from django.contrib.auth import get_user_model

# Загрузка токена
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FSM
class OrderState(StatesGroup):
    waiting_for_bouquet_name = State()
    waiting_for_address = State()
    waiting_for_comment = State()

# Создаём роутер
router = Router()

# Start command
@router.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(OrderState.waiting_for_bouquet_name)
    await message.answer("Здравствуйте! Давайте оформим заказ. Как называется букет?")

# Обработка имени букета
@router.message(OrderState.waiting_for_bouquet_name)
async def bouquet_name_handler(message: types.Message, state: FSMContext):
    bouquet_name = message.text.strip()
    try:
        flower = Bouquet.objects.get(name__iexact=bouquet_name)
        await state.update_data(flower_id=flower.id)

        if flower.image:
            image_path = flower.image.path
            photo = FSInputFile(image_path)
            await message.answer_photo(photo, caption=f"Вы выбрали букет: {flower.name}\nЦена: {flower.price}₽")
        else:
            await message.answer(f"Вы выбрали букет: {flower.name}\nЦена: {flower.price}₽")

        await state.set_state(OrderState.waiting_for_address)
        await message.answer("Укажите адрес доставки:")

    except Bouquet.DoesNotExist:
        await message.answer("Букет с таким названием не найден. Попробуйте снова.")

# Адрес
@router.message(OrderState.waiting_for_address)
async def address_handler(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    await state.set_state(OrderState.waiting_for_comment)
    await message.answer("Добавьте комментарий или отправьте '-' если без комментариев:")

# Комментарий и оформление
@router.message(OrderState.waiting_for_comment)
async def comment_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    flower_id = data.get("flower_id")
    address = data.get("address")
    comment = message.text.strip()

    flower = Bouquet.objects.get(id=flower_id)
    user = get_user_model().objects.first()  # Для демонстрации
    Order.objects.create(
        user=user,
        bouquet=flower,
        delivery_address=address,
        comment='' if comment == '-' else comment
    )

    await message.answer("Ваш заказ оформлен! Спасибо!")
    await state.clear()

def send_order_notification(bouquet, order):
    import requests
    from .credentials import BOT_TOKEN, CHAT_ID

    text = (
        f"📦 Новый заказ!\n\n"
        f"💐 Букет: {bouquet.name}\n"
        f"💰 Цена: {order.total_price} ₽\n"
        f"📅 Доставка: {order.delivery_datetime.strftime('%d.%m.%Y %H:%M')}\n"
        f"📍 Адрес: {order.delivery_address}\n"
        f"📝 Комментарий: {order.comment or 'нет'}"
    )

    image_path = bouquet.image.path if bouquet.image else None
    telegram_api_url = f'https://api.telegram.org/bot{BOT_TOKEN}'

    if image_path:
        with open(image_path, 'rb') as photo_file:
            requests.post(
                f'{telegram_api_url}/sendPhoto',
                data={
                    'chat_id': CHAT_ID,
                    'caption': text
                },
                files={'photo': photo_file}
            )
    else:
        requests.post(
            f'{telegram_api_url}/sendMessage',
            data={'chat_id': CHAT_ID, 'text': text}
        )

# Главная точка входа
async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
