@echo off
echo Запуск Django-сервера...
start cmd /k "venv\Scripts\activate && python manage.py runserver"

timeout /t 5

echo Запуск Telegram-бота...
start cmd /k "venv\Scripts\activate && cd telegram_bot && python bot.py"
