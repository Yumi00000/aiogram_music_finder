from aiogram import Router, F
from aiogram.types import Message

from bot.repositories.history_repo import get_history_by_user_id
from bot.repositories.song_repo import find_song_by_acrid
from bot.services.telegram_formatter import format_song_for_telegram

router = Router(name="history")


@router.message(F.text == "📜 History")
async def history_handler(message: Message):
    """Handle history-related messages."""
    history = await get_history_by_user_id(message.from_user.id)
    if not history:
        await message.answer("You have no history yet.")
        return
    response = "Your recognition history:\n\n"
    for record in history:
        song = await find_song_by_acrid(record.song_id)
        response += format_song_for_telegram(song) + "\n\n"
        response += f"Recognized at: {record.recognized_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        response += "-----------------------\n"
    await message.answer(response)