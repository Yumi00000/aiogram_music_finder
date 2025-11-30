import pytest
from utils.telegram_formatter import format_song_for_telegram
from schemas.SongSchema import SongSchema


@pytest.fixture
def complete_song_schema():
    """Pytest fixture for complete SongSchema."""
    return SongSchema(
        title="Complete Song",
        artist="Complete Artist",
        album="Complete Album",
        release_date="2025-01-01",
        genre="Pop",
        duration=180000,
        links={
            "spotify": "https://open.spotify.com/track/complete",
            "youtube": "https://www.youtube.com/watch?v=complete",
            "deezer": "https://www.deezer.com/track/complete",
        },
    )


@pytest.fixture
def minimal_song_dict():
    """Pytest fixture for minimal song dict."""
    return {"title": "Minimal Song", "artist": "Minimal Artist"}


class TestFormatSongForTelegram:
    """Test format_song_for_telegram function using pytest."""

    def test_format_song_with_complete_fixture(self, complete_song_schema):
        """Test formatting with complete SongSchema fixture."""
        result = format_song_for_telegram(complete_song_schema)

        assert "🎵 *Title*: Complete Song" in result
        assert "🎤 *Artists*: Complete Artist" in result
        assert "💿 *Album*: Complete Album" in result
        assert "📅 *Release Date*: 2025-01-01" in result
        assert "🎼 *Genre*: Pop" in result
        assert "🔗 *Links*:" in result
        assert "[Spotify]" in result
        assert "[YouTube]" in result
        assert "[Deezer]" in result

    def test_format_song_with_minimal_fixture(self, minimal_song_dict):
        """Test formatting with minimal dict fixture."""
        result = format_song_for_telegram(minimal_song_dict)

        assert "Minimal Song" in result
        assert "Minimal Artist" in result

    @pytest.mark.parametrize(
        "song_data,expected_in_result",
        [
            ({"title": "Test1", "artist": "Artist1", "album": "Album1"}, ["Test1", "Artist1", "Album1"]),
            ({"title": "Test2", "artist": "Artist2", "genre": "Rock"}, ["Test2", "Artist2", "Rock"]),
            ({"title": "Test3", "release_date": "2024-01-01"}, ["Test3", "2024-01-01"]),
        ],
    )
    def test_format_song_with_various_dicts(self, song_data, expected_in_result):
        """Test formatting with various dict configurations using parametrize."""
        result = format_song_for_telegram(song_data)

        for expected in expected_in_result:
            assert expected in result

    @pytest.mark.parametrize(
        "title,artist,album,genre",
        [
            ("Title1", "Artist1", "Album1", "Pop"),
            ("Title2", "Artist2", "Album2", "Rock"),
            ("Title3", "Artist3", "Album3", "Jazz"),
        ],
    )
    def test_format_song_schemas(self, title, artist, album, genre):
        """Test formatting with various SongSchema combinations using parametrize."""
        song = SongSchema(title=title, artist=artist, album=album, genre=genre)
        result = format_song_for_telegram(song)

        assert title in result
        assert artist in result
        assert album in result
        assert genre in result

    @pytest.mark.parametrize(
        "field,value,expected_unknown",
        [
            ("artist", None, True),
            ("album", None, True),
            ("release_date", None, True),
            ("genre", None, True),
            ("artist", "Valid Artist", False),
        ],
    )
    def test_format_song_missing_fields(self, field, value, expected_unknown):
        """Test formatting with missing/None fields using parametrize."""
        song = {"title": "Test", field: value}
        result = format_song_for_telegram(song)

        if expected_unknown:
            assert "Unknown" in result
        else:
            assert value in result if value else True

    @pytest.mark.parametrize(
        "links,expected_platforms,not_expected_platforms",
        [
            ({"spotify": "url1"}, ["Spotify"], ["YouTube", "Deezer"]),
            ({"youtube": "url2"}, ["YouTube"], ["Spotify", "Deezer"]),
            ({"deezer": "url3"}, ["Deezer"], ["Spotify", "YouTube"]),
            ({"spotify": "url1", "youtube": "url2"}, ["Spotify", "YouTube"], ["Deezer"]),
            ({"spotify": "url1", "youtube": "url2", "deezer": "url3"}, ["Spotify", "YouTube", "Deezer"], []),
        ],
    )
    def test_format_song_various_link_combinations(self, links, expected_platforms, not_expected_platforms):
        """Test formatting with various link combinations using parametrize."""
        song = SongSchema(title="Test Song", artist="Test Artist", links=links)
        result = format_song_for_telegram(song)

        # Check expected platforms are present
        for platform in expected_platforms:
            assert platform in result

        # Check not expected platforms are absent
        for platform in not_expected_platforms:
            assert platform not in result

    @pytest.mark.parametrize(
        "links,should_have_links_section",
        [
            ({}, False),
            (None, False),
            ({"spotify": "url"}, True),
            ({"youtube": "url"}, True),
            ({"spotify": "url1", "deezer": "url2"}, True),
        ],
    )
    def test_format_song_links_section_presence(self, links, should_have_links_section):
        """Test presence of links section using parametrize."""
        song_data = {"title": "Test", "artist": "Artist"}
        if links is not None:
            song_data["links"] = links

        result = format_song_for_telegram(song_data)

        if should_have_links_section:
            assert "🔗 *Links*:" in result
        else:
            assert "🔗 *Links*:" not in result

    @pytest.mark.parametrize(
        "emoji,field_name",
        [
            ("🎵", "Title"),
            ("🎤", "Artists"),
            ("💿", "Album"),
            ("📅", "Release Date"),
            ("🎼", "Genre"),
        ],
    )
    def test_format_song_emojis_present(self, minimal_song_dict, emoji, field_name):
        """Test that all emojis are present using parametrize."""
        result = format_song_for_telegram(minimal_song_dict)
        assert emoji in result
        assert field_name in result

    @pytest.mark.parametrize(
        "input_data",
        [
            {"title": "", "artist": None, "album": None, "release_date": None, "genre": None},
            {"title": "Only Title"},
            {"title": "Title", "artist": "Artist"},
        ],
    )
    def test_format_song_handles_partial_data(self, input_data):
        """Test formatting with partial data using parametrize."""
        result = format_song_for_telegram(input_data)

        # Should not raise exception
        assert isinstance(result, str)
        assert len(result) > 0

        # Should have basic structure
        assert "🎵" in result
        assert "🎤" in result

    @pytest.mark.parametrize(
        "platform_url",
        [
            "https://open.spotify.com/track/test123",
            "https://www.youtube.com/watch?v=video123",
            "https://www.deezer.com/track/deezer123",
        ],
    )
    def test_format_song_link_urls_present(self, platform_url):
        """Test that platform URLs are present in markdown links using parametrize."""
        links = {}
        if "spotify" in platform_url:
            links["spotify"] = platform_url
        elif "youtube" in platform_url:
            links["youtube"] = platform_url
        elif "deezer" in platform_url:
            links["deezer"] = platform_url

        song = SongSchema(title="Test", artist="Artist", links=links)
        result = format_song_for_telegram(song)

        assert platform_url in result


# Интеграционные тесты
class TestFormatSongIntegration:
    """Integration tests for telegram formatter using pytest."""

    @pytest.mark.parametrize(
        "complete_song",
        [
            {
                "title": "Integration Test 1",
                "artist": "Artist A, Artist B",
                "album": "Album A",
                "release_date": "2024-01-01",
                "genre": "Pop, Rock",
                "links": {
                    "spotify": "https://open.spotify.com/track/123",
                    "youtube": "https://www.youtube.com/watch?v=456",
                },
            },
            {
                "title": "Integration Test 2",
                "artist": "Solo Artist",
                "album": "Solo Album",
                "release_date": "2025-01-01",
                "genre": "Jazz",
                "links": {"deezer": "https://www.deezer.com/track/789"},
            },
        ],
    )
    def test_format_complete_songs(self, complete_song):
        """Test formatting complete songs using parametrize."""
        result = format_song_for_telegram(complete_song)

        # Verify all expected content
        assert complete_song["title"] in result
        assert complete_song["artist"] in result
        assert complete_song["album"] in result
        assert complete_song["release_date"] in result
        assert complete_song["genre"] in result

        # Verify links section exists
        assert "🔗 *Links*:" in result

        # Verify structure
        assert "🎵" in result
        assert "🎤" in result
        assert "💿" in result
