import asyncio
import json
import logging
import os
from typing import Dict, Optional

from acrcloud.recognizer import ACRCloudRecognizer

from bot.core.configure import ACCESS_KEY, ACCESS_SECRET

logger = logging.getLogger(__name__)


class AudioRecognition:
    def __init__(self):
        """Initialize the ACRCloud recognizer with the provided configuration."""
        self.config = {
            "host": "identify-eu-west-1.acrcloud.com",
            "access_key": ACCESS_KEY,
            "access_secret": ACCESS_SECRET,
            "debug": True,
            "timeout": 10,
        }
        self.acrcloud = ACRCloudRecognizer(self.config)

    def recognize_audio(self, file_path: str) -> str:
        """Send an audio file to ACRCloud for recognition."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        result = self.acrcloud.recognize_audio(file_path, 5)
        logger.info(f"ACRCloud API response: {result}")
        return result

    async def recognize_audio_async(self, file_path: str) -> str:
        """Run the recognition asynchronously."""
        return await asyncio.to_thread(self.recognize_audio, file_path)

    @staticmethod
    def format_song_for_telegram(song_info: Dict[str, Optional[str]]) -> str:
        """Format song details into a Telegram-friendly message with emojis."""
        title = song_info.get("title", "Unknown Title")
        artists = ", ".join(song_info.get("artists", ["Unknown Artist"]))
        album = song_info.get("album", "Unknown Album")
        release_date = song_info.get("release_date", "Unknown Date")
        label = song_info.get("label", "Unknown Label")
        links = song_info.get("links", {})

        # Format the message with emojis and Markdown
        message = (
            f"🎵 *Title*: {title}\n"
            f"🎤 *Artists*: {artists}\n"
            f"💿 *Album*: {album}\n"
            f"📅 *Release Date*: {release_date}\n"
            f"🏷️ *Label*: {label}\n"
        )

        # Add links if available
        if links:
            message += "\n🔗 *Links*:\n"
            if "deezer" in links:
                message += f"🎧 [Deezer]({links['deezer']})\n"
            if "spotify" in links:
                message += f"🎶 [Spotify]({links['spotify']})\n"
            if "youtube" in links:
                message += f"📺 [YouTube]({links['youtube']})\n"

        return message

    @staticmethod
    async def get_formatted_response(file_path: str) -> str:
        """Format and return extracted song details as a Telegram-friendly message."""
        try:
            # Perform audio recognition asynchronously
            response = await AudioRecognition().recognize_audio_async(file_path)
            data = json.loads(response)  # Convert JSON string to dict

            # Check if the response contains valid metadata
            if data.get("status", {}).get("code") != 0:
                logger.warning(f"ACRCloud API returned an error: {data.get('status', {}).get('msg')}")
                return "❌ Sorry, the song could not be recognized. Please try again with a clearer audio sample."

            # Extract song details from the response
            songs = data.get("metadata", {}).get("music", [])
            if not songs:
                return "❌ No matching song found. Please try again with a different audio sample."

            # Format the first recognized song
            song_info = {
                "title": songs[0].get("title", "Unknown Title"),
                "artists": [artist["name"] for artist in songs[0].get("artists", [])],
                "album": songs[0].get("album", {}).get("name", "Unknown Album"),
                "release_date": songs[0].get("release_date", "Unknown Date"),
                "label": songs[0].get("label", "Unknown Label"),
                "links": {},  # To store available external links
            }

            # Extract external links from metadata
            external_metadata = songs[0].get("external_metadata", {})
            for platform, platform_data in external_metadata.items():
                if platform == "deezer":
                    song_info["links"]["deezer"] = f"https://www.deezer.com/track/{platform_data['track']['id']}"
                elif platform == "spotify":
                    song_info["links"]["spotify"] = f"https://open.spotify.com/track/{platform_data['track']['id']}"
                elif platform == "youtube":
                    song_info["links"]["youtube"] = f"https://www.youtube.com/watch?v={platform_data['vid']}"

            # Format the song details for Telegram
            return AudioRecognition.format_song_for_telegram(song_info)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse ACRCloud response: {e}")
            return "❌ An error occurred while processing the audio. Please try again later."
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return "❌ An unexpected error occurred. Please try again later."
