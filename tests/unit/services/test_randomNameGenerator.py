import pytest

from bot.services.randomNameGenerator import generate_random_filename


class TestRandomNameGenerator:
    """Test random filename generator."""

    @pytest.mark.asyncio
    async def test_generate_random_filename_length(self):
        """Test that generated filename has correct length."""
        filename = await generate_random_filename()
        assert len(filename) == 24

    @pytest.mark.asyncio
    async def test_generate_random_filename_uniqueness(self):
        """Test that generated filenames are unique."""
        filenames = [await generate_random_filename() for _ in range(100)]
        assert len(filenames) == len(set(filenames))

    @pytest.mark.asyncio
    async def test_generate_random_filename_format(self):
        """Test that generated filename contains only alphanumeric characters."""
        filename = await generate_random_filename()
        assert filename.isalnum()
