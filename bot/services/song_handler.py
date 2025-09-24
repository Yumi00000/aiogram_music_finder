import logging
from bot.services.audioRecognition import AudioRecognition
from bot.services.song_parser import parse_song
from bot.services.telegram_formatter import format_song_for_telegram
from bot.repositories.song_repo import create_song

logger = logging.getLogger(__name__)


async def handle_recognized_song(file_path: str) -> str:
    audio_service = AudioRecognition()

    duration = audio_service.calculate_song_length(file_path)
    if duration < 10:
        return "❌ Sorry, the song could not be recognized. Please send longer audio."

    try:
        data = await audio_service.recognize_audio_async(file_path)
    except Exception as e:
        logger.error(f"Recognition error: {e}")
        return "❌ Error while recognizing audio."

    if data.get("status", {}).get("code") != 0:
        logger.warning(f"ACRCloud error: {data.get('status', {}).get('msg')}")
        return "❌ Song could not be recognized. Please try again."

    songs = data.get("metadata", {}).get("music", []) or data.get("metadata", {}).get("humming", [])
    if not songs:
        return "❌ No matching song found."

    song_info = parse_song(songs[0])

    try:
        await create_song(**song_info)
    except Exception as e:
        logger.error(f"DB save error: {e}")

    return format_song_for_telegram(song_info)
