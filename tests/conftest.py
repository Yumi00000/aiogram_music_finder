import os

# Set test environment variables FIRST, before ANY imports
os.environ.setdefault("DB_USER", "test_user")
os.environ.setdefault("DB_PASS", "test_password")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_NAME", "test_db")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("TELEGRAM_TOKEN", "1234567890:TEST_TOKEN")
os.environ.setdefault("ACRCLOUD_ACCESS_KEY", "test_access_key")
os.environ.setdefault("ACRCLOUD_SECRET_KEY", "test_secret_key")

import asyncio
import sys
from pathlib import Path

import pytest


# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))



@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_bot():
    """Mock bot instance for testing."""
    from unittest.mock import AsyncMock

    bot = AsyncMock()
    bot.get_file = AsyncMock()
    bot.download_file = AsyncMock()
    bot.token = "test_token"
    return bot


@pytest.fixture
def mock_message():
    """Mock message instance for testing."""
    from unittest.mock import AsyncMock, MagicMock

    message = AsyncMock()
    message.from_user = MagicMock()
    message.from_user.id = 123456789
    message.from_user.username = "test_user"
    message.answer = AsyncMock()
    message.bot = MagicMock()
    message.content_type = "audio"
    return message


@pytest.fixture
def sample_acr_response():
    """Sample ACRCloud API response."""
    return {
        "status": {"code": 0, "msg": "Success"},
        "metadata": {
            "music": [
                {
                    "title": "Test Song",
                    "artists": [{"name": "Test Artist"}],
                    "album": {"name": "Test Album"},
                    "release_date": "2024-01-01",
                    "duration_ms": 180000,
                    "genres": [{"name": "Pop"}],
                    "acrid": "test_acrid_123",
                    "external_metadata": {
                        "spotify": {"track": {"id": "spotify_id_123"}},
                        "youtube": {"vid": "youtube_id_123"},
                        "deezer": {"track": {"id": "deezer_id_123"}},
                    },
                }
            ]
        },
    }


@pytest.fixture
def sample_song_info():
    """Sample parsed song information."""
    return {
        "title": "Test Song",
        "artists": "Test Artist",
        "album": "Test Album",
        "release_date": "2024-01-01",
        "duration_ms": 180000,
        "genres": "Pop",
        "acrid": "test_acrid_123",
        "links": {
            "spotify": "https://open.spotify.com/track/spotify_id_123",
            "youtube": "https://www.youtube.com/watch?v=youtube_id_123",
            "deezer": "https://www.deezer.com/track/deezer_id_123",
        },
    }
