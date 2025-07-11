import os
import sys
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import django

# Django setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flower_project.settings")
django.setup()

from main.models import Bouquet, Order
from django.contrib.auth import get_user_model
from telegram_bot.credentials import BOT_TOKEN, CHAT_ID

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FSM состояния
class OrderState(StatesGroup):
    waiting_for_bouquet_name = State()
    waiting_for_address = State()
    waiting_for_datetime = State()
    waiting_for_comment = State()

router = Router()

# /start
@router.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(OrderState.waiting_for_bouquet_name)
    await message.answer("Здравствуйте! Как называется букет, который вы хотите заказать?")

# Название букета
@router.message(OrderState.waiting_for_bouquet_name)
async def bouquet_name_handler(message: types.Message, state: FSMContext):
    name = message.text.strip()
    try:
        flower = Bouquet.objects.get(name__iexact=name)
        await state.update_data(flower_id=flower.id)

        if flower.image and os.path.exists(flower.image.path):
            photo = FSInputFile(flower.image.path)
            await message.answer_photo(photo, caption=f"Вы выбрали букет: {flower.name}\nЦена: {flower.price}₽")
        else:
            await message.answer(f"Вы выбрали букет: {flower.name}\nЦена: {flower.price}₽")

        await state.set_state(OrderState.waiting_for_address)
        await message.answer("Укажите адрес доставки:")

    except Exception as e:
        logger.error(f"Ошибка при обработке букета: {e}")
        await message.answer("Произошла ошибка при обработке букета. Попробуйте снова или выберите другой букет.")

# Адрес
@router.message(OrderState.waiting_for_address)
async def address_handler(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    await state.set_state(OrderState.waiting_for_datetime)
    await message.answer("Укажите дату и время доставки (в формате: 2025-07-11 15:00):")

# Дата и время
@router.message(OrderState.waiting_for_datetime)
async def datetime_handler(message: types.Message, state: FSMContext):
    from datetime import datetime
    try:
        dt = datetime.strptime(message.text.strip(), "%Y-%m-%d %H:%M")
        await state.update_data(delivery_datetime=dt)
        await state.set_state(OrderState.waiting_for_comment)
        await message.answer("Добавьте комментарий или отправьте '-' если без комментариев:")
    except ValueError:
        await message.answer("Неверный формат даты. Пример: 2025-07-11 15:00")

# Комментарий и оформление
@router.message(OrderState.waiting_for_comment)
async def comment_handler(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        flower = Bouquet.objects.get(id=data["flower_id"])
        user = get_user_model().objects.first()
        comment = message.text.strip()
        order = Order.objects.create(
            user=user,
            delivery_address=data["address"],
            delivery_datetime=data["delivery_datetime"],
            comment='' if comment == '-' else comment,
            total_price=flower.price
        )
        order.bouquets.add(flower)

        # Отправка сообщения магазину
        caption = (
            f"🌸 Новый заказ!\n"
            f"Букет: {flower.name}\n"
            f"💰 Цена: {flower.price} ₽\n"
            f"📍 Адрес: {data['address']}\n"
            f"📅 Доставка: {data['delivery_datetime']:%d.%m.%Y %H:%M}\n"
            f"📝 Комментарий: {comment if comment != '-' else 'Нет'}"
        )

        try:
            if flower.image and os.path.exists(flower.image.path):
                photo = FSInputFile(flower.image.path)
                await message.answer_photo(photo, caption=f"Вы выбрали букет: {flower.name}\nЦена: {flower.price}₽")
            else:
                await message.answer(f"Вы выбрали букет: {flower.name}\nЦена: {flower.price}₽")
        except Exception as e:
            logger.error(f"Ошибка с изображением: {e}")
            await message.answer(f"Букет: {flower.name}\nЦена: {flower.price}₽ (фото недоступно)")

    except Exception as e:
        logger.error(f"Ошибка при оформлении заказа: {e}")
        await message.answer("Что-то пошло не так. Попробуйте ещё раз.")

# Запуск
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
