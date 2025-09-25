from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboard.menu import menu_keyboard

from bot.repositories.user_repo import create_user

# Create a router for the start handler
router = Router(name="start")


@router.message(Command(commands=["start"]))
async def start_handler(message: Message):
    """Send a welcome message with the menu keyboard."""
    user_id = message.from_user.id
    username = message.from_user.username or "there"
    await create_user(user_id, username)
    await message.answer(
        "Welcome to the Music Recognition Bot! 🎶\n" "Click the button below to recognize a song:",
        reply_markup=menu_keyboard,
    )
