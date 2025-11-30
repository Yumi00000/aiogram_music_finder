from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from aiogram.enums import ContentType
from aiogram.types import Message

from bot.handlers.recognizerHandler import recognize_song_button, recognize_song


class TestRecognizerHandler:
    """Test recognizer handler."""

    @pytest.mark.asyncio
    async def test_recognize_song_button(self, mock_message):
        """Test recognize song button handler."""
        await recognize_song_button(mock_message)

        mock_message.answer.assert_called_once()
        call_args = mock_message.answer.call_args
        assert "Please send an audio" in call_args[0][0]
        assert "at least 10 seconds" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_recognize_song_too_short(self):
        """Test recognition with file too short."""
        message = AsyncMock(spec=Message)
        message.from_user = MagicMock()
        message.from_user.id = 123456
        message.from_user.username = "test_user"
        message.content_type = ContentType.AUDIO
        message.answer = AsyncMock()

        # Create mock audio file
        audio = MagicMock()
        audio.duration = 5
        audio.file_id = "short_file_123"
        message.audio = audio

        await recognize_song(message)

        message.answer.assert_called_once()
        call_args = message.answer.call_args
        assert "at least 10 seconds" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_recognize_song_success(self):
        """Test successful song recognition."""
        message = AsyncMock(spec=Message)
        message.from_user = MagicMock()
        message.from_user.id = 123456
        message.from_user.username = "test_user"
        message.content_type = ContentType.AUDIO
        message.answer = AsyncMock()
        message.bot = AsyncMock()

        # Create mock audio file
        audio = MagicMock()
        audio.duration = 30
        audio.file_id = "audio_file_123"
        message.audio = audio

        with patch("bot.handlers.recognizerHandler.create_user") as mock_create_user, patch(
            "bot.handlers.recognizerHandler.generate_random_filename", return_value="random123"
        ), patch("bot.handlers.recognizerHandler.convert") as mock_convert, patch(
            "bot.handlers.recognizerHandler.handle_recognized_song"
        ) as mock_handle, patch(
            "bot.handlers.recognizerHandler.create_history"
        ) as mock_create_history, patch(
            "os.remove"
        ) as mock_remove:
            mock_convert.save_and_convert_to_mp3 = AsyncMock(return_value="/path/to/file.mp3")
            mock_handle.return_value = ("🎵 Song found!", "song_123")

            await recognize_song(message)

            mock_create_user.assert_called_once_with(123456, "test_user")
            mock_convert.save_and_convert_to_mp3.assert_called_once()
            mock_handle.assert_called_once_with("/path/to/file.mp3")
            mock_create_history.assert_called_once_with(123456, "song_123")
            mock_remove.assert_called_once_with("/path/to/file.mp3")

            message.answer.assert_called_once()
            assert "🎵 Song found!" in message.answer.call_args[0][0]

    @pytest.mark.asyncio
    async def test_recognize_song_with_exception(self):
        """Test recognition with exception."""
        message = AsyncMock(spec=Message)
        message.from_user = MagicMock()
        message.from_user.id = 123456
        message.answer = AsyncMock()
        message.from_user.username = "test_user"
        message.content_type = ContentType.AUDIO

        audio = MagicMock()
        audio.duration = 30
        audio.file_id = "audio_file_123"
        message.audio = audio

        with patch("bot.handlers.recognizerHandler.create_user", side_effect=Exception("DB Error")):
            await recognize_song(message)

            message.answer.assert_called_once()
            assert "❌ An error occurred:" in message.answer.call_args[0][0]

    @pytest.mark.asyncio
    async def test_recognize_song_voice(self):
        """Test recognition with voice message."""
        message = AsyncMock(spec=Message)
        message.from_user = MagicMock()
        message.from_user.id = 123456
        message.answer = AsyncMock()
        message.from_user.username = "test_user"
        message.content_type = ContentType.VOICE
        message.bot = AsyncMock()

        voice = MagicMock()
        voice.duration = 15
        voice.file_id = "voice_file_123"
        message.voice = voice

        with patch("bot.handlers.recognizerHandler.create_user"), patch(
            "bot.handlers.recognizerHandler.generate_random_filename", return_value="random456"
        ), patch("bot.handlers.recognizerHandler.convert") as mock_convert, patch(
            "bot.handlers.recognizerHandler.handle_recognized_song"
        ) as mock_handle, patch(
            "bot.handlers.recognizerHandler.create_history"
        ), patch(
            "os.remove"
        ):
            mock_convert.save_and_convert_to_mp3 = AsyncMock(return_value="/path/to/voice.mp3")
            mock_handle.return_value = ("🎵 Voice recognized!", "voice_song_123")

            await recognize_song(message)

            message.answer.assert_called_once()
            assert "🎵 Voice recognized!" in message.answer.call_args[0][0]

    @pytest.mark.asyncio
    async def test_recognize_song_no_duration(self):
        """Test recognition with file without duration attribute."""
        message = AsyncMock(spec=Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock()
        message.from_user.id = 123456
        message.from_user.username = "test_user"
        message.content_type = ContentType.AUDIO

        audio = MagicMock()
        # No duration attribute
        del audio.duration
        audio.file_id = "audio_file_123"
        message.audio = audio

        await recognize_song(message)

        # Should fail because duration is 0
        message.answer.assert_called_once()
        assert "at least 10 seconds" in message.answer.call_args[0][0]
