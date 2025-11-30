import pytest

from utils.song_parser import parse_song


@pytest.fixture
def minimal_acr_song():
    """Pytest fixture for minimal ACR song data."""
    return {"title": "Minimal Song"}


@pytest.fixture
def complete_acr_song():
    """Pytest fixture for complete ACR song data."""
    return {
        "title": "Complete Song",
        "artists": [{"name": "Artist 1"}, {"name": "Artist 2"}],
        "album": {"name": "Album Name"},
        "release_date": "2025-01-01",
        "duration_ms": 200000,
        "genres": [{"name": "Pop"}, {"name": "Rock"}],
        "acrid": "test_acrid",
        "external_metadata": {
            "spotify": {"track": {"id": "spotify123"}},
            "youtube": {"vid": "youtube456"},
            "deezer": {"track": {"id": "deezer789"}},
        },
    }


class TestParseSong:
    """Test parse_song function using pytest."""

    def test_parse_song_with_complete_data(self, sample_acr_response):
        """Test parsing with complete ACR response data using fixture."""
        acr_song = sample_acr_response["metadata"]["music"][0]
        result = parse_song(acr_song)

        assert result["title"] == "Test Song"
        assert result["artists"] == "Test Artist"
        assert result["album"] == "Test Album"
        assert result["release_date"] == "2024-01-01"
        assert result["duration_ms"] == 180000
        assert result["genres"] == "Pop"
        assert result["acrid"] == "test_acrid_123"
        assert "spotify" in result["links"]
        assert "youtube" in result["links"]
        assert "deezer" in result["links"]

    def test_parse_song_with_fixture(self, complete_acr_song):
        """Test parsing using custom fixture."""
        result = parse_song(complete_acr_song)

        assert result["title"] == "Complete Song"
        assert result["artists"] == "Artist 1, Artist 2"
        assert result["album"] == "Album Name"
        assert result["genres"] == "Pop, Rock"

    @pytest.mark.parametrize(
        "acr_data,field,expected",
        [
            ({}, "title", "Unknown Title"),
            ({"title": "Test"}, "artists", "Unknown Artist"),
            ({"title": "Test"}, "release_date", "Unknown Date"),
            ({"title": "Test"}, "genres", "Unknown Genre"),
            ({"title": "Test", "artists": []}, "artists", ""),
        ],
    )
    def test_parse_song_missing_fields(self, acr_data, field, expected):
        """Test parsing with various missing fields using parametrize."""
        result = parse_song(acr_data)
        assert result[field] == expected

    @pytest.mark.parametrize(
        "album_input,expected",
        [
            ({"name": "Album Name"}, "Album Name"),
            ("String Album", "String Album"),
            (None, None),
            ({}, "Unknown Album"),
        ],
    )
    def test_parse_song_album_formats(self, minimal_acr_song, album_input, expected):
        """Test parsing with various album formats using parametrize."""
        minimal_acr_song["album"] = album_input
        result = parse_song(minimal_acr_song)

        if expected is None:
            assert result["album"] in [None, "Unknown Album"]
        else:
            assert result["album"] == expected

    @pytest.mark.parametrize(
        "artists_input,expected",
        [
            ([{"name": "Artist 1"}], "Artist 1"),
            ([{"name": "A1"}, {"name": "A2"}], "A1, A2"),
            ([{"name": "A"}, {"name": "B"}, {"name": "C"}], "A, B, C"),
            ([], ""),
            ("String Artist", "String Artist"),
            (None, "Unknown Artist"),
        ],
    )
    def test_parse_song_artists_formats(self, minimal_acr_song, artists_input, expected):
        """Test parsing with various artists formats using parametrize."""
        if artists_input is not None:
            minimal_acr_song["artists"] = artists_input
        result = parse_song(minimal_acr_song)
        assert result["artists"] == expected

    @pytest.mark.parametrize(
        "platform,track_id,expected_url",
        [
            ("spotify", "abc123", "https://open.spotify.com/track/abc123"),
            ("spotify", "xyz789", "https://open.spotify.com/track/xyz789"),
            ("youtube", "vid123", "https://www.youtube.com/watch?v=vid123"),
            ("youtube", "vid456", "https://www.youtube.com/watch?v=vid456"),
            ("deezer", "track123", "https://www.deezer.com/track/track123"),
            ("deezer", "track456", "https://www.deezer.com/track/track456"),
        ],
    )
    def test_parse_song_individual_links(self, minimal_acr_song, platform, track_id, expected_url):
        """Test parsing individual platform links using parametrize."""
        if platform == "spotify":
            minimal_acr_song["external_metadata"] = {"spotify": {"track": {"id": track_id}}}
        elif platform == "youtube":
            minimal_acr_song["external_metadata"] = {"youtube": {"vid": track_id}}
        elif platform == "deezer":
            minimal_acr_song["external_metadata"] = {"deezer": {"track": {"id": track_id}}}

        result = parse_song(minimal_acr_song)
        assert result["links"][platform] == expected_url

    @pytest.mark.parametrize(
        "platforms,expected_count",
        [
            (["spotify"], 1),
            (["spotify", "youtube"], 2),
            (["spotify", "youtube", "deezer"], 3),
            (["youtube", "deezer"], 2),
            ([], 0),
        ],
    )
    def test_parse_song_multiple_links(self, minimal_acr_song, platforms, expected_count):
        """Test parsing with various link combinations using parametrize."""
        external_metadata = {}

        if "spotify" in platforms:
            external_metadata["spotify"] = {"track": {"id": "spot123"}}
        if "youtube" in platforms:
            external_metadata["youtube"] = {"vid": "yt123"}
        if "deezer" in platforms:
            external_metadata["deezer"] = {"track": {"id": "dz123"}}

        minimal_acr_song["external_metadata"] = external_metadata
        result = parse_song(minimal_acr_song)

        assert len(result["links"]) == expected_count
        for platform in platforms:
            assert platform in result["links"]

    @pytest.mark.parametrize(
        "genres_input,expected",
        [
            ([{"name": "Pop"}], "Pop"),
            ([{"name": "Rock"}, {"name": "Jazz"}], "Rock, Jazz"),
            ([], ""),
            ("String Genre", "String Genre"),
            (None, "Unknown Genre"),
        ],
    )
    def test_parse_song_genres_formats(self, minimal_acr_song, genres_input, expected):
        """Test parsing with various genres formats using parametrize."""
        if genres_input is not None:
            minimal_acr_song["genres"] = genres_input
        result = parse_song(minimal_acr_song)
        assert result["genres"] == expected

    @pytest.mark.parametrize(
        "field_name,field_value",
        [
            ("duration_ms", 180000),
            ("duration_ms", 240000),
            ("acrid", "test_id_123"),
            ("acrid", "another_id_456"),
        ],
    )
    def test_parse_song_optional_fields(self, minimal_acr_song, field_name, field_value):
        """Test parsing optional fields using parametrize."""
        minimal_acr_song[field_name] = field_value
        result = parse_song(minimal_acr_song)
        assert result[field_name] == field_value

    def test_parse_song_with_no_metadata(self, minimal_acr_song):
        """Test parsing without external metadata using fixture."""
        result = parse_song(minimal_acr_song)
        assert result["links"] == {}

    @pytest.mark.parametrize(
        "release_date",
        [
            "2024-01-01",
            "2025-12-31",
            "2023-06-15",
            None,
        ],
    )
    def test_parse_song_release_dates(self, minimal_acr_song, release_date):
        """Test parsing with various release dates using parametrize."""
        if release_date:
            minimal_acr_song["release_date"] = release_date
            result = parse_song(minimal_acr_song)
            assert result["release_date"] == release_date
        else:
            result = parse_song(minimal_acr_song)
            assert result["release_date"] == "Unknown Date"


class TestParseSongIntegration:
    """Integration tests for parse_song using pytest."""

    @pytest.mark.parametrize(
        "complete_data",
        [
            {
                "title": "Integration Test 1",
                "artists": [{"name": "Artist A"}],
                "album": {"name": "Album A"},
                "release_date": "2024-01-01",
                "genres": [{"name": "Pop"}],
                "external_metadata": {"spotify": {"track": {"id": "123"}}},
            },
            {
                "title": "Integration Test 2",
                "artists": [{"name": "Artist B"}, {"name": "Artist C"}],
                "album": "String Album",
                "release_date": "2025-01-01",
                "genres": [{"name": "Rock"}, {"name": "Jazz"}],
                "external_metadata": {"spotify": {"track": {"id": "456"}}, "youtube": {"vid": "789"}},
            },
        ],
    )
    def test_parse_complete_songs(self, complete_data):
        """Test parsing complete song data using parametrize."""
        result = parse_song(complete_data)

        assert result["title"] == complete_data["title"]
        assert "Unknown" not in result["title"]
        assert "Unknown" not in result["artists"]
        assert len(result["links"]) > 0
