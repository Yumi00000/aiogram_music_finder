import os
from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import Message
from bot.keyboard.menu import menu_keyboard
from bot.repositories.history_repo import create_history
from bot.repositories.user_repo import create_user
from bot.services.audioConverter import ConvertMusic
from bot.services.audioRecognition import AudioRecognition
from bot.services.randomNameGenerator import generate_random_filename
from utils.song_handler import handle_recognized_song

router = Router(name="recognizer")
recognizer = AudioRecognition()
convert = ConvertMusic()


@router.message(F.text == "🎵 Recognize Song")
async def recognize_song_button(message: Message):
    """Handle the 'Recognize Song' button press."""
    await message.answer(
        "Please send an audio, voice, video, or video note file to recognize the song.\n\n"
        "⏱️ Note: The file must be at least 10 seconds long for accurate recognition.",
        reply_markup=menu_keyboard,
    )


@router.message(F.content_type.in_({ContentType.AUDIO, ContentType.VOICE, ContentType.VIDEO, ContentType.VIDEO_NOTE}))
async def recognize_song(message: Message):
    """Handle incoming media files for song recognition."""
    content_type = message.content_type
    try:
        # Get the file object based on content type
        file = getattr(message, content_type)

        # Check file duration (must be at least 10 seconds)
        duration = file.duration if hasattr(file, "duration") and file.duration else 0
        if duration < 10:
            await message.answer(
                "⏱️ The media file must be at least 10 seconds long for accurate recognition.\n"
                f"Your file is {duration} seconds.",
                reply_markup=menu_keyboard,
            )
            return

        user_id = message.from_user.id
        username = message.from_user.username

        # Ensure user exists in database before creating history
        await create_user(user_id, username)

        generated_name = await generate_random_filename()
        file_name = f"{generated_name}{user_id}{file.file_id}.{content_type}"
        file_id = file.file_id

        # Convert the media file to MP3
        mp3_file_path = await convert.save_and_convert_to_mp3(file_id, file_name, message.bot)

        # Recognize the song from the MP3 file
        response, song_id = await handle_recognized_song(mp3_file_path)
        await create_history(user_id, song_id)
        os.remove(mp3_file_path)
        # Send the response to the user
        await message.answer(response, reply_markup=menu_keyboard)
    except Exception as e:
        await message.answer(f"❌ An error occurred: {e}", reply_markup=menu_keyboard)
