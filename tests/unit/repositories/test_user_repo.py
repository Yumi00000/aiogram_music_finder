from unittest.mock import patch, AsyncMock, MagicMock

import pytest

from bot.repositories.user_repo import get_user_by_telegram_id, update_user_status, create_user
from models import UserModel


@pytest.fixture
def mock_session():
    """Pytest fixture for mock database session."""
    session = AsyncMock()
    session.add = MagicMock()

    begin_context = AsyncMock()
    begin_context.__aenter__ = AsyncMock(return_value=None)
    begin_context.__aexit__ = AsyncMock(return_value=None)
    session.begin = MagicMock(return_value=begin_context)

    return session


@pytest.fixture
def mock_sessionmaker(mock_session):
    """Pytest fixture for mock sessionmaker."""
    with patch("bot.repositories.user_repo.sessionmaker") as mock_sm:
        # Правильная настройка async context manager для sessionmaker
        context = AsyncMock()
        context.__aenter__ = AsyncMock(return_value=mock_session)
        context.__aexit__ = AsyncMock(return_value=None)
        mock_sm.return_value = context
        yield mock_sm


class TestUserRepository:
    """Test user repository functions using pytest."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "telegram_id,username,expected_active",
        [
            (123456, "test_user", True),
            (789012, "another_user", True),
            (111222, "user3", True),
        ],
    )
    async def test_create_user_new_user(self, mock_sessionmaker, telegram_id, username, expected_active):
        """Test creating new users with various data using parametrize."""
        with patch("bot.repositories.user_repo.get_user_by_telegram_id", return_value=None):
            await create_user(telegram_id, username)

            mock_session = await mock_sessionmaker.return_value.__aenter__()
            mock_session.add.assert_called_once()
            added_user = mock_session.add.call_args[0][0]
            assert isinstance(added_user, UserModel)
            assert added_user.telegram_id == telegram_id
            assert added_user.username == username
            assert added_user.is_active is expected_active

    @pytest.mark.asyncio
    @pytest.mark.parametrize("telegram_id", [123456, 789012, 999999])
    async def test_create_user_existing_user(self, telegram_id):
        """Test creating users that already exist using parametrize."""
        existing_user = MagicMock(spec=UserModel)

        with patch("bot.repositories.user_repo.get_user_by_telegram_id", return_value=existing_user), patch(
            "bot.repositories.user_repo.update_user_status"
        ) as mock_update:

            await create_user(telegram_id, "test_user")

            mock_update.assert_called_once_with(telegram_id, True)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "telegram_id,user_exists",
        [
            (123456, True),
            (789012, True),
            (999999, False),
        ],
    )
    async def test_get_user_by_telegram_id(self, mock_sessionmaker, telegram_id, user_exists):
        """Test getting users by telegram_id using parametrize."""
        mock_user = MagicMock(spec=UserModel) if user_exists else None

        mock_session = await mock_sessionmaker.return_value.__aenter__()

        mock_scalars = MagicMock()
        mock_scalars.first = MagicMock(return_value=mock_user)

        mock_result = MagicMock()
        mock_result.scalars = MagicMock(return_value=mock_scalars)

        mock_session.execute = AsyncMock(return_value=mock_result)

        user = await get_user_by_telegram_id(telegram_id)

        if user_exists:
            assert user == mock_user
        else:
            assert user is None

    @pytest.mark.asyncio
    async def test_get_user_by_telegram_id_found(self, mock_sessionmaker):
        """Test getting an existing user using fixture."""
        mock_user = MagicMock(spec=UserModel)

        mock_session = await mock_sessionmaker.return_value.__aenter__()

        mock_scalars = MagicMock()
        mock_scalars.first = MagicMock(return_value=mock_user)

        mock_result = MagicMock()
        mock_result.scalars = MagicMock(return_value=mock_scalars)

        mock_session.execute = AsyncMock(return_value=mock_result)

        user = await get_user_by_telegram_id(123456)

        assert user == mock_user

    @pytest.mark.asyncio
    async def test_get_user_by_telegram_id_not_found(self, mock_sessionmaker):
        """Test getting a non-existent user using fixture."""
        mock_session = await mock_sessionmaker.return_value.__aenter__()

        mock_scalars = MagicMock()
        mock_scalars.first = MagicMock(return_value=None)

        mock_result = MagicMock()
        mock_result.scalars = MagicMock(return_value=mock_scalars)

        mock_session.execute = AsyncMock(return_value=mock_result)

        user = await get_user_by_telegram_id(999999)

        assert user is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "telegram_id,new_status,old_status",
        [
            (123456, True, False),
            (789012, False, True),
            (111222, True, True),
        ],
    )
    async def test_update_user_status(self, mock_sessionmaker, telegram_id, new_status, old_status):
        """Test updating user status with various states using parametrize."""
        mock_user = MagicMock(spec=UserModel)
        mock_user.is_active = old_status

        mock_session = await mock_sessionmaker.return_value.__aenter__()

        mock_scalars = MagicMock()
        mock_scalars.first = MagicMock(return_value=mock_user)

        mock_result = MagicMock()
        mock_result.scalars = MagicMock(return_value=mock_scalars)

        mock_session.execute = AsyncMock(return_value=mock_result)

        await update_user_status(telegram_id, new_status)

        assert mock_user.is_active == new_status
        mock_session.add.assert_called_once_with(mock_user)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("telegram_id", [999999, 111111, 222222])
    async def test_update_user_status_user_not_found(self, mock_sessionmaker, telegram_id):
        """Test updating status for non-existent users using parametrize."""
        mock_session = await mock_sessionmaker.return_value.__aenter__()

        mock_scalars = MagicMock()
        mock_scalars.first = MagicMock(return_value=None)

        mock_result = MagicMock()
        mock_result.scalars = MagicMock(return_value=mock_scalars)

        mock_session.execute = AsyncMock(return_value=mock_result)

        await update_user_status(telegram_id, True)

        # Should not raise error, just do nothing
        mock_session.add.assert_not_called()


class TestUserRepositoryIntegration:
    """Integration tests for user repository using pytest."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "scenario",
        [
            {"telegram_id": 123, "username": "user1", "exists": False},
            {"telegram_id": 456, "username": "user2", "exists": True},
        ],
    )
    async def test_create_user_workflow(self, scenario):
        """Test complete user creation workflow using parametrize."""
        telegram_id = scenario["telegram_id"]
        username = scenario["username"]
        existing_user = MagicMock(spec=UserModel) if scenario["exists"] else None

        with patch("bot.repositories.user_repo.get_user_by_telegram_id", return_value=existing_user), patch(
            "bot.repositories.user_repo.update_user_status"
        ) as mock_update:

            # Настройка sessionmaker мока
            with patch("bot.repositories.user_repo.sessionmaker") as mock_sm:
                mock_session = AsyncMock()
                mock_session.add = MagicMock()

                begin_context = AsyncMock()
                begin_context.__aenter__ = AsyncMock(return_value=None)
                begin_context.__aexit__ = AsyncMock(return_value=None)
                mock_session.begin = MagicMock(return_value=begin_context)

                session_context = AsyncMock()
                session_context.__aenter__ = AsyncMock(return_value=mock_session)
                session_context.__aexit__ = AsyncMock(return_value=None)
                mock_sm.return_value = session_context

                await create_user(telegram_id, username)

                if scenario["exists"]:
                    # Should update existing user
                    mock_update.assert_called_once_with(telegram_id, True)
                else:
                    # Should create new user
                    mock_session.add.assert_called_once()
