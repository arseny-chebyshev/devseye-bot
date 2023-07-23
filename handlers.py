from aiogram import types
from aiogram_dialog import DialogManager
from states import SettingState
from db.models import Settings
from loader import dp


@dp.message_handler(commands='start')
async def start(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(SettingState.start)


@dp.message_handler(chat_type=[types.ChatType.CHANNEL])
async def notify_subscribers(message: types.Message):
    subscribed_users = Settings.filter_vacancy_recipients(
        vacancy_text=message.text)
    for user in subscribed_users:
        await message.forward(chat_id=user.id)
