from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.create_kb import cars_kb
from state.create import CreateState
import os
from utils.database import Database  # Предполагается, что у вас есть модуль utils.database и класс Database


async def create_cars_salle(message: Message, state: FSMContext, bot: Bot):
    # Создаем подключение к базе данных
    db = Database(os.getenv(
        "DATABASE_NAME"))  # Предполагается, что у вас есть переменная окружения DATABASE_NAME с именем базы данных
    cars = db.db_select_all("cars")

    # Создаем клавиатуру на основе данных из базы данных
    kb = cars_kb(cars)

    # Отправляем сообщение с клавиатурой
    await bot.send_message(message.from_user.id, "Выберите интересующий автомобиль из нашего автопарка",
                           reply_markup=kb)

    # Устанавливаем состояние
    await state.set_state(CreateState.cars)