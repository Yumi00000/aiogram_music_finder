from aiogram import Router, F, types
from aiogram.types import Message
from bot.repositories.history_repo import get_history_by_user_id
from bot.repositories.song_repo import find_song_by_acrid
from bot.repositories.user_repo import create_user
from utils.slice_response import paginate_response
from utils.telegram_formatter import format_song_for_telegram

router = Router(name="history")


@router.message(F.text == "📜 History")
async def history_handler(message: Message):
    # Ensure user exists in database
    await create_user(message.from_user.id, message.from_user.username)
    history = await get_history_by_user_id(message.from_user.id)
    if not history:
        await message.answer("You have no history yet.")
        return
    items = []
    for record in history:
        song = await find_song_by_acrid(record.song_id)
        text = format_song_for_telegram(song)
        text += f"\n🕒 Recognized at: {record.recognized_at.strftime('%Y-%m-%d %H:%M:%S')}"
        items.append(text)
    response, kb = paginate_response(items, page=0)
    await message.answer(response, reply_markup=kb, parse_mode="Markdown")


@router.callback_query(F.data.startswith("history:"))
async def history_page(call: types.CallbackQuery):
    page = int(call.data.split(":")[1])
    history = await get_history_by_user_id(call.from_user.id)
    items = []
    for record in history:
        song = await find_song_by_acrid(record.song_id)
        text = format_song_for_telegram(song)
        text += f"\n🕒 Recognized at: {record.recognized_at.strftime('%Y-%m-%d %H:%M:%S')}"
        items.append(text)
    response, kb = paginate_response(items, page=page)
    await call.message.edit_text(response, reply_markup=kb, parse_mode="Markdown")
