import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.core.configure import bot_token
from bot.handlers.recognizerHandler import router as recognize_song_router
from bot.handlers.startHandler import router as start_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load your Telegram bot token from a secure location


async def main():
    # Initialize the bot and dispatcher
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()

    # Register handlers
    dp.include_router(recognize_song_router)
    dp.include_router(start_router)
    # Start polling for updates
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
