from aiogram.fsm.state import StatesGroup, State


class CreateState(StatesGroup):
    cars = State()
    salle = State()
    date = State()
    price = State()
