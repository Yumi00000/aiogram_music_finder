from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from bot.services.audioConverter import ConvertMusic


class TestConvertMusic:
    """Test ConvertMusic class."""

    @pytest.mark.asyncio
    async def test_convert_success(self):
        """Test successful audio conversion."""
        with patch("asyncio.create_subprocess_exec") as mock_subprocess:
            mock_process = AsyncMock()
            mock_process.communicate = AsyncMock(return_value=(b"stdout", b""))
            mock_process.returncode = 0
            mock_subprocess.return_value = mock_process

            result = await ConvertMusic.convert("input.mp4", "output.mp3")

            assert result == "output.mp3"
            mock_subprocess.assert_called_once()
            # Verify ffmpeg was called with correct arguments
            call_args = mock_subprocess.call_args[0]
            assert call_args[0] == "ffmpeg"
            assert "-i" in call_args
            assert "input.mp4" in call_args
            assert "output.mp3" in call_args

    @pytest.mark.asyncio
    async def test_convert_failure(self):
        """Test audio conversion failure."""
        with patch("asyncio.create_subprocess_exec") as mock_subprocess:
            mock_process = AsyncMock()
            mock_process.communicate = AsyncMock(return_value=(b"", b"Error message"))
            mock_process.returncode = 1
            mock_subprocess.return_value = mock_process

            with pytest.raises(RuntimeError, match="FFmpeg conversion failed"):
                await ConvertMusic.convert("input.mp4", "output.mp3")

    @pytest.mark.asyncio
    async def test_convert_with_exception(self):
        """Test audio conversion with exception."""
        with patch("asyncio.create_subprocess_exec", side_effect=Exception("Test error")):
            with pytest.raises(Exception, match="Test error"):
                await ConvertMusic.convert("input.mp4", "output.mp3")

    @pytest.mark.asyncio
    async def test_save_and_convert_to_mp3_success(self):
        """Test successful file download and conversion."""
        mock_bot = AsyncMock()
        mock_file = MagicMock()
        mock_file.file_path = "path/to/file"
        mock_bot.get_file = AsyncMock(return_value=mock_file)
        mock_bot.download_file = AsyncMock()

        with patch("bot.services.audioConverter.settings") as mock_settings, patch.object(
            ConvertMusic, "convert", new=AsyncMock(return_value="/downloads/test.mp4.mp3")
        ) as mock_convert:

            from pathlib import Path

            mock_settings.DOWNLOADS_DIR = Path("/downloads")

            result = await ConvertMusic.save_and_convert_to_mp3("file123", "test.mp4", mock_bot)

            # The result should match what convert returns
            assert result == "/downloads/test.mp4.mp3"
            mock_bot.get_file.assert_called_once_with("file123")
            mock_bot.download_file.assert_called_once()
            mock_convert.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_and_convert_to_mp3_download_failure(self):
        """Test file download failure."""
        mock_bot = AsyncMock()
        mock_bot.get_file = AsyncMock(side_effect=Exception("Download failed"))

        with patch("bot.services.audioConverter.settings") as mock_settings:
            from pathlib import Path

            mock_settings.DOWNLOADS_DIR = Path("/downloads")

            # Function logs exception and re-raises it
            with pytest.raises(Exception, match="Download failed"):
                await ConvertMusic.save_and_convert_to_mp3("file123", "test.mp4", mock_bot)
