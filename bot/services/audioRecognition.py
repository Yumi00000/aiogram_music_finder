import asyncio
import json
import logging
import os
import audioread
from acrcloud.recognizer import ACRCloudRecognizer
from bot.core.configure import settings

logger = logging.getLogger(__name__)

class AudioRecognition:
    def __init__(self):
        self.config = {
            "host": settings.acr_host,
            "access_key": settings.ACRCLOUD_ACCESS_KEY,
            "access_secret": settings.ACRCLOUD_SECRET_KEY,
            "debug": settings.DEBUG,
            "timeout": settings.acr_timeout,
        }
        self.acrcloud = ACRCloudRecognizer(self.config)

    @staticmethod
    def calculate_song_length(song_path: str) -> float:
        with audioread.audio_open(song_path) as audio:
            return audio.duration

    def recognize_audio(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        result = self.acrcloud.recognize_audio(file_path, 5)
        logger.info(f"ACRCloud API response: {result}")
        return result

    async def recognize_audio_async(self, file_path: str) -> dict:
        response = await asyncio.to_thread(self.recognize_audio, file_path)
        return json.loads(response)
