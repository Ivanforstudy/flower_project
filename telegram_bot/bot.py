import logging
import os
import sys
import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
from asgiref.sync import sync_to_async
import django
from datetime import datetime, timedelta

# Django setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flower_project.settings")
django.setup()

from main.models import Bouquet, Order
from django.contrib.auth import get_user_model
from telegram_bot.credentials import BOT_TOKEN, CHAT_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderState(StatesGroup):
    waiting_for_bouquet_name = State()
    waiting_for_address = State()
    waiting_for_datetime = State()
    waiting_for_comment = State()

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(OrderState.waiting_for_bouquet_name)
    await message.answer("Здравствуйте! Как называется букет, который вы хотите заказать?")

@router.message(OrderState.waiting_for_bouquet_name)
async def bouquet_name_handler(message: types.Message, state: FSMContext):
    name = message.text.strip()
    try:
        flower = await sync_to_async(Bouquet.objects.get)(name__iexact=name)
        await state.update_data(flower_id=flower.id)

        logger.info(f"Путь к изображению: {flower.image.path}")

        if flower.image and os.path.exists(flower.image.path):
            photo = FSInputFile(flower.image.path)
            await message.answer_photo(photo, caption=f"Вы выбрали букет: {flower.name}\nЦена: {flower.price}₽")
        else:
            await message.answer(f"Вы выбрали букет: {flower.name}\nЦена: {flower.price}₽ (⚠️ Фото не найдено)")

        await state.set_state(OrderState.waiting_for_address)
        await message.answer("Укажите адрес доставки:")

    except Bouquet.DoesNotExist:
        await message.answer("❗ Букет с таким названием не найден. Попробуйте снова.")
    except Exception as e:
        logger.error(f"Ошибка при обработке букета: {e}")
        await message.answer("Произошла ошибка при обработке букета. Попробуйте снова или выберите другой.")

@router.message(OrderState.waiting_for_address)
async def address_handler(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    await state.set_state(OrderState.waiting_for_datetime)
    await message.answer("Укажите дату и время доставки (в формате: 2025-07-11 15:00):")

@router.message(OrderState.waiting_for_datetime)
async def datetime_handler(message: types.Message, state: FSMContext):
    try:
        dt = datetime.strptime(message.text.strip(), "%Y-%m-%d %H:%M")
        if dt < datetime.now() + timedelta(hours=1):
            await message.answer("❗ Доставку можно оформить минимум за 1 час вперёд.")
            return

        await state.update_data(delivery_datetime=dt)
        await state.set_state(OrderState.waiting_for_comment)
        await message.answer("Добавьте комментарий или отправьте '-' если без комментариев:")
    except ValueError:
        await message.answer("Неверный формат даты. Пример: 2025-07-11 15:00")

@router.message(OrderState.waiting_for_comment)
async def comment_handler(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        flower = await sync_to_async(Bouquet.objects.get)(id=data["flower_id"])

        User = get_user_model()
        user, _ = await sync_to_async(User.objects.get_or_create)(
            email=f"tg_{message.from_user.id}@example.com",
            defaults={"name": message.from_user.full_name or "Telegram User"}
        )

        comment = message.text.strip()

        order = await sync_to_async(Order.objects.create)(
            user=user,
            delivery_address=data["address"],
            delivery_datetime=data["delivery_datetime"],
            comment='' if comment == '-' else comment,
            total_price=flower.price
        )
        await sync_to_async(order.bouquets.add)(flower)

        caption = (
            f"\U0001F490 Новый заказ!\n"
            f"Букет: {flower.name}\n"
            f"\U0001F4B0 Цена: {flower.price} ₽\n"
            f"\U0001F4CD Адрес: {data['address']}\n"
            f"\U0001F4C5 Доставка: {data['delivery_datetime']:%d.%m.%Y %H:%M}\n"
            f"\U0001F4DD Комментарий: {comment if comment != '-' else 'Нет'}"
        )

        if flower.image and os.path.exists(flower.image.path):
            photo = FSInputFile(flower.image.path)
            await message.bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=caption)
        else:
            await message.bot.send_message(chat_id=CHAT_ID, text=caption)

        await message.answer("✅ Ваш заказ оформлен. Спасибо!")
        await state.clear()

    except Exception as e:
        logger.error(f"Ошибка при оформлении заказа: {e}")
        await message.answer("Что-то пошло не так. Попробуйте ещё раз.")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
