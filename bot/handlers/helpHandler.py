from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboard.menu import menu_keyboard

router = Router(name="help")


@router.message(F.text == "ℹ️ Help")
@router.message(Command(commands=["help"]))
async def help_handler(message: Message):
    """Send help information about the bot."""
    help_text = """
🎵 *Music Recognition Bot - Help Guide*

*How to use:*
1️⃣ Click "🎵 Recognize Song" button
2️⃣ Send an audio, voice, video, or video note file
3️⃣ Wait for the bot to recognize the song
4️⃣ Get the song details with streaming links!

*Requirements:*
⏱️ Media files must be *at least 10 seconds long* for accurate recognition
📁 Supported formats: Audio, Voice, Video, Video Note

*Features:*
✅ Recognizes songs from audio/video files
✅ Provides song title, artist, and album information
✅ Includes links to Spotify, Deezer, and YouTube
✅ Saves recognition history for each user

*Commands:*
/start - Start the bot and show menu
/help - Show this help message

*Buttons:*
🎵 Recognize Song - Start song recognition
📜 History - View your recognition history
ℹ️ Help - Show this help message

*Tips:*
💡 Use clear audio without too much background noise
💡 Longer clips (10-15 seconds) work better
💡 Popular songs are more likely to be recognized

*Need support?*
If you encounter any issues, please contact the bot administrator.

Powered by ACRCloud 🎶
"""
    await message.answer(help_text, reply_markup=menu_keyboard)
