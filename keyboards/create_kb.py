from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import os
from utils.database import Database

def cars_kb():
    db = Database(os.getenv("DATABASE_NAME"))
    cars = db.db_select_all("cars")
    kb = InlineKeyboardBuilder()
    for car in cars:
        kb.add(InlineKeyboardButton(text=car.name_cars, callback_data=car.id))
    return kb
