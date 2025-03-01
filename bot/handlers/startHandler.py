from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboard.menu import menu_keyboard

# Create a router for the start handler
router = Router(name="start")


@router.message(Command(commands=["start"]))
async def start_handler(message: Message):
    """Send a welcome message with the menu keyboard."""
    await message.answer(
        "Welcome to the Music Recognition Bot! 🎶\n" "Click the button below to recognize a song:",
        reply_markup=menu_keyboard,
    )
