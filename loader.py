import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry
from db.models import TelegramChannel
from settings import BOT_TOKEN
from dialogs import settings_dialog


class Bot(aiogram.Bot):

    async def check_subscribtions(self,
                                  user: aiogram.types.User,
                                  for_every_channel: bool = True):
        channels_for_sub = TelegramChannel.objects.all()
        user_statuses = [
            await bot.get_chat_member(
                channel, user.id).status != aiogram.types.ChatMemberStatus.LEFT
                    for channel in channels_for_sub]
        return all(user_statuses) if for_every_channel else any(user_statuses)

bot = Bot(token=BOT_TOKEN)
dp = aiogram.Dispatcher(bot=bot, storage=MemoryStorage())
dialog_registry = DialogRegistry(dp=dp)
dialog_registry.register(settings_dialog)
