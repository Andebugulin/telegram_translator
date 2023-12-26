from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    HISTORY = State()
    WORD = State()
    TRANSLATING = State() 
    MENU = State()