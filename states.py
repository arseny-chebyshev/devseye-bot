from aiogram.dispatcher.filters.state import StatesGroup, State


class SettingState(StatesGroup):
    start = State()
    skills = State()
    level = State()
    employment_type = State()
    locations = State()
    finish = State()
