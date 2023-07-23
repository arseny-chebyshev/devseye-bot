import logging
import aiogram
from loader import dp
import handlers
from middleware import CreateDBUserMiddleware


async def on_startup(dispatcher: aiogram.Dispatcher):
    logger = logging.getLogger('aiogram')
    logger.info(f'Handlers module registered: {handlers}')
    dispatcher.middleware.setup(CreateDBUserMiddleware())


logging.basicConfig(level=logging.DEBUG)
aiogram.executor.start_polling(dispatcher=dp,
                               on_startup=on_startup)
