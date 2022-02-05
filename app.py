from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
import config


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def setup_bot_commands(Bot:bot):
    bot_commands = [
        BotCommand(command="/menu", description="Меню"),
        BotCommand(command="/last", description="Показать посление слова"),
        BotCommand(command="/rand", description="Показать случайные слова"),
        BotCommand(command="/match", description="Игра: соотнести"),
        BotCommand(command="/remember", description="Игра: всмпомнить"),
        BotCommand(command="/type", description="Игра: напечатать"),
        BotCommand(command="/set_fav", description="Добавить в избранное"),
        BotCommand(command="/rem_fav", description="Удалить из избранного"),
    ]
    await bot.set_my_commands(bot_commands)



async def on_shutdown(dp):
    await bot.close()
    await storage.close()

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    from callback_button import dp
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=setup_bot_commands, skip_updates=True)

