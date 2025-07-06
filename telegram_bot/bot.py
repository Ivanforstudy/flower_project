import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
from dotenv import load_dotenv
import django

# Настройка Django окружения
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_project.settings')
django.setup()

from main.models import Flower, Order
from django.contrib.auth import get_user_model

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(bot)

user_states = {}

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_states[message.chat.id] = {'step': 'get_bouquet_name'}
    await message.answer("Здравствуйте! Давайте оформим заказ. Как называется букет?")

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text_handler(message: types.Message):
    chat_id = message.chat.id
    state = user_states.get(chat_id, {})

    if state.get('step') == 'get_bouquet_name':
        bouquet_name = message.text.strip()
        try:
            flower = Flower.objects.get(name__iexact=bouquet_name)
            state['flower'] = flower
            state['step'] = 'get_address'

            if flower.image:
                image_path = flower.image.path
                await bot.send_photo(chat_id, InputFile(image_path), caption=f"Вы выбрали букет: {flower.name}\nЦена: {flower.price}₽")
            else:
                await message.answer(f"Вы выбрали букет: {flower.name}\nЦена: {flower.price}₽")

            await message.answer("Укажите адрес доставки:")
        except Flower.DoesNotExist:
            await message.answer("Букет с таким названием не найден. Попробуйте снова.")

    elif state.get('step') == 'get_address':
        state['address'] = message.text.strip()
        state['step'] = 'get_comment'
        await message.answer("Добавьте комментарий к заказу или отправьте '-' если без комментариев:")

    elif state.get('step') == 'get_comment':
        comment = message.text.strip()
        flower = state.get('flower')
        address = state.get('address')
        user = get_user_model().objects.first()  # Тестовый пользователь

        order = Order.objects.create(
            user=user,
            flower=flower,
            delivery_address=address,
            comment='' if comment == '-' else comment
        )

        await message.answer("Ваш заказ оформлен! Спасибо!")
        user_states.pop(chat_id, None)

if __name__ == '__main__':
    logger.info("Запуск бота...")
    executor.start_polling(dp, skip_updates=True)
