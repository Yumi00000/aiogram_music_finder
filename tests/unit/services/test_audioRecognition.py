import json
from unittest.mock import patch, MagicMock

import pytest

from bot.services.audioRecognition import AudioRecognition


class TestAudioRecognition:
    """Test AudioRecognition class."""

    @pytest.fixture
    def audio_recognition(self):
        """Create an AudioRecognition instance."""
        with patch("bot.services.audioRecognition.settings") as mock_settings:
            mock_settings.acr_host = "test_host"
            mock_settings.ACRCLOUD_ACCESS_KEY = "test_key"
            mock_settings.ACRCLOUD_SECRET_KEY = "test_secret"
            mock_settings.DEBUG = False
            mock_settings.acr_timeout = 10
            return AudioRecognition()

    def test_init(self, audio_recognition):
        """Test AudioRecognition initialization."""
        assert audio_recognition.config["host"] == "test_host"
        assert audio_recognition.config["access_key"] == "test_key"
        assert audio_recognition.config["access_secret"] == "test_secret"
        assert audio_recognition.config["debug"] is False
        assert audio_recognition.config["timeout"] == 10

    @patch("audioread.audio_open")
    def test_calculate_song_length(self, mock_audio_open, audio_recognition):
        """Test calculating song length."""
        mock_audio = MagicMock()
        mock_audio.duration = 123.45
        mock_audio_open.return_value.__enter__.return_value = mock_audio

        duration = audio_recognition.calculate_song_length("test.mp3")

        assert duration == 123.45
        mock_audio_open.assert_called_once_with("test.mp3")

    def test_recognize_audio_file_not_found(self, audio_recognition):
        """Test recognize_audio with non-existent file."""
        with pytest.raises(FileNotFoundError):
            audio_recognition.recognize_audio("non_existent_file.mp3")

    @patch("os.path.exists")
    def test_recognize_audio_success(self, mock_exists, audio_recognition):
        """Test successful audio recognition."""
        mock_exists.return_value = True
        mock_response = {"status": {"code": 0}, "metadata": {}}
        audio_recognition.acrcloud.recognize_audio = MagicMock(return_value=json.dumps(mock_response))

        result = audio_recognition.recognize_audio("test.mp3")

        assert json.loads(result) == mock_response
        audio_recognition.acrcloud.recognize_audio.assert_called_once_with("test.mp3", 5)

    @pytest.mark.asyncio
    @patch("os.path.exists")
    async def test_recognize_audio_async(self, mock_exists, audio_recognition):
        """Test asynchronous audio recognition."""
        mock_exists.return_value = True
        mock_response = {"status": {"code": 0}, "metadata": {"music": []}}
        audio_recognition.acrcloud.recognize_audio = MagicMock(return_value=json.dumps(mock_response))

        result = await audio_recognition.recognize_audio_async("test.mp3")

        assert result == mock_response

    @pytest.mark.asyncio
    @patch("audioread.audio_open")
    async def test_calculate_song_length_with_short_file(self, mock_audio_open, audio_recognition):
        """Test calculating song length for a short file."""
        mock_audio = MagicMock()
        mock_audio.duration = 5.0
        mock_audio_open.return_value.__enter__.return_value = mock_audio

        duration = audio_recognition.calculate_song_length("short.mp3")

        assert duration == 5.0
