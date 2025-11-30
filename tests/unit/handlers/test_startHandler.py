from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from aiogram.types import Message

from bot.handlers.startHandler import start_handler


class TestStartHandler:
    """Test start handler."""

    @pytest.mark.asyncio
    async def test_start_handler(self, mock_message):
        """Test start command handler."""
        with patch("bot.handlers.startHandler.create_user") as mock_create_user:
            mock_create_user.return_value = None

            await start_handler(mock_message)

            mock_create_user.assert_called_once_with(123456789, "test_user")
            mock_message.answer.assert_called_once()

            # Check message content
            call_args = mock_message.answer.call_args
            assert "Welcome to the Music Recognition Bot!" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_start_handler_no_username(self):
        """Test start handler when user has no username."""
        message = AsyncMock(spec=Message)
        message.from_user = MagicMock()
        message.from_user.id = 987654
        message.from_user.username = None
        message.answer = AsyncMock()

        with patch("bot.handlers.startHandler.create_user") as mock_create_user:
            await start_handler(message)

            mock_create_user.assert_called_once_with(987654, "there")
