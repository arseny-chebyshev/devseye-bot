from aiogram.types import Message
from aiogram.dispatcher.middlewares import BaseMiddleware
from db.models import User

class CreateDBUserMiddleware(BaseMiddleware):
    async def on_pre_process_message(self,
                                     message: Message,
                                     *args, **kwargs):
        try:
            user = User.objects.get(id=message.from_user.id)
        except User.DoesNotExist:
            user = User.objects.create(**dict(message.from_user))
