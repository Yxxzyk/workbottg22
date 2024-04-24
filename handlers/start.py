from aiogram import Bot
from aiogram.types import Message
from keyboards.register_kb import register_keyboard
import os
from utils.database import Database
from keyboards.profile_kb import profile_kb

async def get_start(message: Message, bot: Bot):
    db = Database(os.getenv("DATABASE_NAME"))
    users = db.select_user_id(message.from_user.id)
    if(users):
        await bot.send_message(message.from_user.id, f"Здравствуйте, {users.user_name}!", reply_markup=profile_kb)

    else:
        await bot.send_message(message.from_user.id, f"Здравствуйте, <b>{message.from_user.first_name}</b>. Рады приветствовать Вас\n"
                                                 f"Бот поможет создать заявку на прокат автомобиля 🚗 из нашего автопарка\n"
                                                 f"А также, он послужит историей бронирования, ваших эмоциональных 😊 поездок на авто нашего автопарка\n\n"
                                                 f"<b>С уважение, команда CARS&GO</b>", reply_markup=register_keyboard)
