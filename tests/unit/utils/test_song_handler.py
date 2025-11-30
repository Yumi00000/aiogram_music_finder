from unittest.mock import patch, AsyncMock, MagicMock

import pytest

from utils.song_handler import handle_recognized_song


class TestSongHandler:
    """Test song handler functions."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "duration,expected_message",
        [
            (5.0, "❌ Sorry, the song could not be recognized. Please send longer audio."),
            (8.0, "❌ Sorry, the song could not be recognized. Please send longer audio."),
            (9.9, "❌ Sorry, the song could not be recognized. Please send longer audio."),
        ],
    )
    async def test_handle_recognized_song_short_audio(self, duration, expected_message):
        """Test handling audio that's too short with various durations."""
        with patch("utils.song_handler.AudioRecognition") as mock_audio_class:
            mock_audio = MagicMock()
            mock_audio.calculate_song_length.return_value = duration
            mock_audio_class.return_value = mock_audio

            result = await handle_recognized_song("short_audio.mp3")

            assert result == expected_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "exception_type,exception_message",
        [
            (Exception, "API Error"),
            (ConnectionError, "Network failed"),
            (TimeoutError, "Request timeout"),
        ],
    )
    async def test_handle_recognized_song_recognition_errors(self, exception_type, exception_message):
        """Test handling various recognition errors using parametrize."""
        with patch("utils.song_handler.AudioRecognition") as mock_audio_class:
            mock_audio = MagicMock()
            mock_audio.calculate_song_length.return_value = 15.0
            mock_audio.recognize_audio_async = AsyncMock(side_effect=exception_type(exception_message))
            mock_audio_class.return_value = mock_audio

            result = await handle_recognized_song("audio.mp3")

            assert result == "❌ Error while recognizing audio."

    @pytest.mark.asyncio
    async def test_handle_recognized_song_recognition_error(self):
        """Test handling recognition error."""
        with patch("utils.song_handler.AudioRecognition") as mock_audio_class:
            mock_audio = MagicMock()
            mock_audio.calculate_song_length.return_value = 15.0
            mock_audio.recognize_audio_async = AsyncMock(side_effect=Exception("API Error"))
            mock_audio_class.return_value = mock_audio

            result = await handle_recognized_song("audio.mp3")

            assert result == "❌ Error while recognizing audio."

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status_code,status_msg",
        [
            (1001, "No result"),
            (2001, "Decode error"),
            (3001, "Invalid access"),
        ],
    )
    async def test_handle_recognized_song_failed_statuses(self, status_code, status_msg):
        """Test handling various failed recognition statuses using parametrize."""
        with patch("utils.song_handler.AudioRecognition") as mock_audio_class:
            mock_audio = MagicMock()
            mock_audio.calculate_song_length.return_value = 15.0
            mock_audio.recognize_audio_async = AsyncMock(
                return_value={"status": {"code": status_code, "msg": status_msg}}
            )
            mock_audio_class.return_value = mock_audio

            result = await handle_recognized_song("audio.mp3")

            assert result == "❌ Song could not be recognized. Please try again."

    @pytest.mark.asyncio
    async def test_handle_recognized_song_failed_status(self):
        """Test handling failed recognition status."""
        with patch("utils.song_handler.AudioRecognition") as mock_audio_class:
            mock_audio = MagicMock()
            mock_audio.calculate_song_length.return_value = 15.0
            mock_audio.recognize_audio_async = AsyncMock(return_value={"status": {"code": 1001, "msg": "No result"}})
            mock_audio_class.return_value = mock_audio

            result = await handle_recognized_song("audio.mp3")

            assert result == "❌ Song could not be recognized. Please try again."

    @pytest.mark.asyncio
    async def test_handle_recognized_song_no_songs_found(self):
        """Test handling when no songs are found."""
        with patch("utils.song_handler.AudioRecognition") as mock_audio_class:
            mock_audio = MagicMock()
            mock_audio.calculate_song_length.return_value = 15.0
            mock_audio.recognize_audio_async = AsyncMock(return_value={"status": {"code": 0}, "metadata": {}})
            mock_audio_class.return_value = mock_audio

            result = await handle_recognized_song("audio.mp3")

            assert result == "❌ No matching song found."

    @pytest.mark.asyncio
    async def test_handle_recognized_song_success(self, sample_acr_response, sample_song_info):
        """Test successful song recognition."""
        with patch("utils.song_handler.AudioRecognition") as mock_audio_class, patch(
            "utils.song_handler.create_song"
        ) as mock_create_song:
            mock_audio = MagicMock()
            mock_audio.calculate_song_length.return_value = 15.0
            mock_audio.recognize_audio_async = AsyncMock(return_value=sample_acr_response)
            mock_audio_class.return_value = mock_audio

            mock_song = MagicMock()
            mock_song.acrid = "test_acrid_123"
            mock_create_song.return_value = mock_song

            response, song_id = await handle_recognized_song("audio.mp3")

            assert "🎵 *Title*: Test Song" in response
            assert song_id == "test_acrid_123"
            mock_create_song.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_recognized_song_with_humming(self):
        """Test handling humming recognition."""
        with patch("utils.song_handler.AudioRecognition") as mock_audio_class, patch(
            "utils.song_handler.create_song"
        ) as mock_create_song:
            mock_audio = MagicMock()
            mock_audio.calculate_song_length.return_value = 15.0
            mock_audio.recognize_audio_async = AsyncMock(
                return_value={
                    "status": {"code": 0},
                    "metadata": {
                        "humming": [
                            {"title": "Hummed Song", "artists": [{"name": "Hummed Artist"}], "acrid": "humming_123"}
                        ]
                    },
                }
            )
            mock_audio_class.return_value = mock_audio

            mock_song = MagicMock()
            mock_song.acrid = "humming_123"
            mock_create_song.return_value = mock_song

            response, song_id = await handle_recognized_song("audio.mp3")

            assert "🎵 *Title*:" in response
            assert song_id == "humming_123"
