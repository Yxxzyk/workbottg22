from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from state.register import RegisterState
import re
import os
from utils.database import Database


async def start_register(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv("DATABASE_NAME"))
    users = db.select_user_id(message.from_user.id)
    if users:
        await bot.send_message(message.from_user.id, f"<b>{users.user_name}</b> \n<b>Вы уже зарегистрированы.</b> ")
    else:
        await bot.send_message(message.from_user.id, f"Давайте приступим к регистрации\n Для начала скажите как к Вам обращаться ?")
        await state.set_state(RegisterState.regName)


async def register_name(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f"😊Приятно познакомиться {message.text}\n"
                                                  f"Теперь укажите номер телефона, чтобы узнавать об акциях в первых рядах\n"
                                                  f"📱Формат телефона: +7-XXX-XXX-XX-XX, для упрощения ввода можете без тире и слитно\n"
                                                  f"⚠️Внимание ! Я чувствителен к формату.")
    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.regPhone)


async def register_phone(message: Message, state: FSMContext, bot: Bot):
    if re.findall("^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$", message.text):
        await state.update_data(regphone=message.text)
        await bot.send_message(message.from_user.id, "Отлично! Теперь укажите ваш email.")
        await state.set_state(RegisterState.regEmail)
    else:
        await bot.send_message(message.from_user.id, "Номер указан в неправильном формате")


async def register_email(message: Message, state: FSMContext, bot: Bot):
    if re.match(r"[^@]+@[^@]+\.[^@]+", message.text):
        await state.update_data(regemail=message.text)
        reg_data = await state.get_data()
        reg_name = reg_data.get("regname")
        reg_phone = reg_data.get("regphone")
        reg_email = reg_data.get("regemail")
        msg = f"Приятно познакомиться {reg_name} \n\n Телефон - {reg_phone} \n\n Email - {reg_email}"
        await bot.send_message(message.from_user.id, msg)
        db = Database(os.getenv("DATABASE_NAME"))
        db.add_user(reg_name, reg_phone, message.from_user.id, reg_email)
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, "Email указан в неправильном формате")
