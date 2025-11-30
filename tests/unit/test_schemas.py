import pytest
from schemas.SongSchema import SongSchema


class TestSongSchema:
    """Test SongSchema."""

    def test_song_schema_creation(self):
        """Test creating a SongSchema instance."""
        song = SongSchema(
            title="Test Song",
            artist="Test Artist",
            album="Test Album",
            release_date="2024-01-01",
            genre="Pop",
            duration=180000,
            links={"spotify": "https://spotify.com/track/123"},
        )

        assert song.title == "Test Song"
        assert song.artist == "Test Artist"
        assert song.album == "Test Album"
        assert song.release_date == "2024-01-01"
        assert song.genre == "Pop"
        assert song.duration == 180000
        assert song.links == {"spotify": "https://spotify.com/track/123"}

    @pytest.mark.parametrize(
        "field,value",
        [
            ("title", "Minimal Song"),
            ("artist", None),
            ("album", None),
            ("release_date", None),
            ("genre", None),
            ("duration", None),
            ("links", None),
        ],
    )
    def test_song_schema_optional_fields(self, field, value):
        """Test SongSchema with various optional fields using parametrize."""
        song = SongSchema(title="Minimal Song")

        if field == "title":
            assert song.title == value
        else:
            assert getattr(song, field) == value

    def test_song_schema_with_optional_fields(self):
        """Test creating a SongSchema with optional fields."""
        song = SongSchema(title="Minimal Song")

        assert song.title == "Minimal Song"
        assert song.artist is None
        assert song.album is None
        assert song.release_date is None
        assert song.genre is None
        assert song.duration is None
        assert song.links is None

    @pytest.mark.parametrize(
        "data,expected_title,expected_artist",
        [
            ({"title": "Dict Song", "artist": "Dict Artist"}, "Dict Song", "Dict Artist"),
            ({"title": "Only Title"}, "Only Title", None),
            ({"title": "With Album", "album": "Album"}, "With Album", None),
        ],
    )
    def test_song_schema_from_various_dicts(self, data, expected_title, expected_artist):
        """Test creating SongSchema from various dictionaries using parametrize."""
        song = SongSchema(**data)
        assert song.title == expected_title
        assert song.artist == expected_artist

    def test_song_schema_from_dict(self):
        """Test creating a SongSchema from dictionary."""
        data = {"title": "Dict Song", "artist": "Dict Artist", "album": "Dict Album"}

        song = SongSchema(**data)

        assert song.title == "Dict Song"
        assert song.artist == "Dict Artist"
        assert song.album == "Dict Album"

    def test_song_schema_with_empty_string_title(self):
        """Test SongSchema with empty string title."""
        song = SongSchema(title="", artist="Artist")

        assert song.title == ""
        assert song.artist == "Artist"

    def test_song_schema_model_dump(self):
        """Test converting SongSchema to dictionary."""
        song = SongSchema(title="Test Song", artist="Test Artist")

        data = song.model_dump()

        assert data["title"] == "Test Song"
        assert data["artist"] == "Test Artist"
        assert "album" in data
        assert "links" in data

    @pytest.fixture
    def sample_song(self):
        """Pytest fixture for sample song - demonstrates fixture usage."""
        return SongSchema(title="Fixture Song", artist="Fixture Artist", genre="Rock")

    def test_song_schema_with_fixture(self, sample_song):
        """Test using pytest fixture."""
        assert sample_song.title == "Fixture Song"
        assert sample_song.artist == "Fixture Artist"
        assert sample_song.genre == "Rock"
