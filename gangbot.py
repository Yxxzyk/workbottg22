from aiogram import Bot, Dispatcher, F
import asyncio

from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os
from aiogram.filters import Command

from utils.commands import set_commands
from handlers.start import get_start
from state.register import RegisterState
from handlers.register import start_register, register_name, register_phone, register_email
from handlers.admin.create import create_cars_salle
from filters.CheckAdmin import CheckAdmin

load_dotenv()

token = os.getenv("TOKEN")
admin_id = os.getenv("ADMIN_ID")

bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

async def start_bot(bot: Bot):
    await bot.send_message(799142949, text="Я готов к работе")

dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands="start"))


#Регистрируем хендлеры регистрации
dp.message.register(start_register, F.text=="Регистрация")
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_phone, RegisterState.regPhone)
dp.message.register(register_email, RegisterState.regEmail)

#Регистрируем хендлеры создания скидок на авто из автопарка проката
dp.message.register(create_cars_salle, Command(commands="create"), CheckAdmin())

async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_updtes=True)
    finally:
        await bot.session.close()

async def main():
    await start()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())