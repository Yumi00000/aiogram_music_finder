import asyncio
import os
import logging

logger = logging.getLogger(__name__)


class ConvertMusic:
    @staticmethod
    async def convert(temp_file_path: str, mp3_file_path: str) -> str:
        """Convert an audio file to MP3 format using FFmpeg."""
        try:
            process = await asyncio.create_subprocess_exec(
                "ffmpeg",
                "-i",
                temp_file_path,  # Input file
                "-t",
                "15",  # Limit duration to 15 seconds
                "-ar",
                "8000",  # Set sample rate to 8000 Hz
                "-ac",
                "1",  # Set mono channel
                "-b:a",
                "64k",  # Set bitrate to 64 kbps
                mp3_file_path,  # Output file
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                logger.error(f"FFmpeg conversion failed: {stderr.decode()}")
                raise RuntimeError(f"FFmpeg conversion failed: {stderr.decode()}")

            logger.info(f"File converted successfully: {mp3_file_path}")
            return mp3_file_path

        except Exception as e:
            logger.error(f"Error during audio conversion: {e}")
            raise

    @staticmethod
    async def save_and_convert_to_mp3(file_id: str, file_name: str, bot) -> str:
        """Download a file and convert it to MP3 format."""
        temp_file_path = f"../downloads/{file_name}"
        try:
            # Get file info
            file_path = await bot.get_file(file_id)

            # Save the file temporarily

            await bot.download_file(file_path.file_path, destination=temp_file_path)

            # Convert the file to MP3
            mp3_file_path = f"../downloads/{file_name}.mp3"
            await ConvertMusic.convert(temp_file_path, mp3_file_path)

            return mp3_file_path

        except Exception as e:
            logger.error(f"Error during file processing: {e}")
            raise
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                logger.info(f"Temporary file removed: {temp_file_path}")
