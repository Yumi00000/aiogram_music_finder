"""
Unit tests for utils/helpers.py using pytest framework.
All tests use pytest features: parametrize, fixtures, marks.
"""

import pytest
from utils.helpers import safe_artists, safe_genres


@pytest.fixture
def sample_artists_list():
    """Pytest fixture for sample artists list."""
    return [{"name": "Artist 1"}, {"name": "Artist 2"}]


@pytest.fixture
def sample_genres_list():
    """Pytest fixture for sample genres list."""
    return [{"name": "Pop"}, {"name": "Rock"}]


class TestSafeArtists:
    """Test safe_artists function using pytest."""

    @pytest.mark.parametrize(
        "artists_data,expected",
        [
            ([{"name": "Artist 1"}, {"name": "Artist 2"}], "Artist 1, Artist 2"),
            ([{"name": "Solo Artist"}], "Solo Artist"),
            ([{"name": "A"}, {"name": "B"}, {"name": "C"}], "A, B, C"),
        ],
    )
    def test_safe_artists_with_list_of_dicts(self, artists_data, expected):
        """Test with various artist list configurations using parametrize."""
        result = safe_artists(artists_data)
        assert result == expected

    def test_safe_artists_with_fixture(self, sample_artists_list):
        """Test using pytest fixture."""
        result = safe_artists(sample_artists_list)
        assert result == "Artist 1, Artist 2"

    @pytest.mark.parametrize(
        "string_input",
        [
            "Single Artist",
            "Another Artist",
            "Test Artist Name",
        ],
    )
    def test_safe_artists_with_strings(self, string_input):
        """Test with various string inputs using parametrize."""
        result = safe_artists(string_input)
        assert result == string_input

    @pytest.mark.parametrize(
        "invalid_input,expected",
        [
            (None, "Unknown Artist"),
            (123, "Unknown Artist"),
            (456.789, "Unknown Artist"),
            (True, "Unknown Artist"),
            (False, "Unknown Artist"),
            ({"name": "dict"}, "Unknown Artist"),
            ({"id": 1}, "Unknown Artist"),
        ],
    )
    def test_safe_artists_with_invalid_types(self, invalid_input, expected):
        """Test with various invalid input types using pytest parametrize."""
        result = safe_artists(invalid_input)
        assert result == expected

    @pytest.mark.parametrize(
        "empty_input,expected",
        [
            ([], ""),
            ("", ""),
        ],
    )
    def test_safe_artists_with_empty_values(self, empty_input, expected):
        """Test with empty values using parametrize."""
        result = safe_artists(empty_input)
        assert result == expected

    @pytest.mark.parametrize(
        "artists_data,expected",
        [
            ([{"id": 1}, {"name": "Artist 2"}], "Unknown Artist, Artist 2"),
            ([{"id": 1}, {"id": 2}, {"name": "Artist 3"}], "Unknown Artist, Unknown Artist, Artist 3"),
            ([{"other": "field"}, {"name": "Valid"}], "Unknown Artist, Valid"),
        ],
    )
    def test_safe_artists_with_missing_name_key(self, artists_data, expected):
        """Test with dictionaries missing 'name' key using parametrize."""
        result = safe_artists(artists_data)
        assert result == expected


class TestSafeGenres:
    """Test safe_genres function using pytest."""

    @pytest.mark.parametrize(
        "genres_data,expected",
        [
            ([{"name": "Pop"}, {"name": "Rock"}], "Pop, Rock"),
            ([{"name": "Jazz"}], "Jazz"),
            ([{"name": "Classical"}, {"name": "Hip-Hop"}, {"name": "Electronic"}], "Classical, Hip-Hop, Electronic"),
        ],
    )
    def test_safe_genres_with_list_of_dicts(self, genres_data, expected):
        """Test with various genre list configurations using parametrize."""
        result = safe_genres(genres_data)
        assert result == expected

    def test_safe_genres_with_fixture(self, sample_genres_list):
        """Test using pytest fixture."""
        result = safe_genres(sample_genres_list)
        assert result == "Pop, Rock"

    @pytest.mark.parametrize(
        "string_input",
        [
            "Pop",
            "Rock",
            "Jazz",
            "Classical Music",
        ],
    )
    def test_safe_genres_with_strings(self, string_input):
        """Test with various string inputs using parametrize."""
        result = safe_genres(string_input)
        assert result == string_input

    @pytest.mark.parametrize(
        "invalid_input,expected",
        [
            (None, "Unknown Genre"),
            (456, "Unknown Genre"),
            (123.456, "Unknown Genre"),
            (False, "Unknown Genre"),
            (True, "Unknown Genre"),
            ({"name": "dict"}, "Unknown Genre"),
            ({"id": 1}, "Unknown Genre"),
        ],
    )
    def test_safe_genres_with_invalid_types(self, invalid_input, expected):
        """Test with various invalid input types using pytest parametrize."""
        result = safe_genres(invalid_input)
        assert result == expected

    @pytest.mark.parametrize(
        "empty_input,expected",
        [
            ([], ""),
            ("", ""),
        ],
    )
    def test_safe_genres_with_empty_values(self, empty_input, expected):
        """Test with empty values using parametrize."""
        result = safe_genres(empty_input)
        assert result == expected

    @pytest.mark.parametrize(
        "genres_data,expected",
        [
            ([{"id": 1}, {"name": "Rock"}], "Unknown Genre, Rock"),
            ([{"id": 1}, {"id": 2}, {"name": "Jazz"}], "Unknown Genre, Unknown Genre, Jazz"),
            ([{"other": "field"}, {"name": "Valid"}], "Unknown Genre, Valid"),
        ],
    )
    def test_safe_genres_with_missing_name_key(self, genres_data, expected):
        """Test with dictionaries missing 'name' key using parametrize."""
        result = safe_genres(genres_data)
        assert result == expected


class TestHelpersIntegration:
    """Integration tests for helpers functions using pytest."""

    @pytest.mark.parametrize(
        "artists,genres,expected_artists,expected_genres",
        [
            ([{"name": "Artist"}], [{"name": "Pop"}], "Artist", "Pop"),
            (None, None, "Unknown Artist", "Unknown Genre"),
            ([], [], "", ""),
            ("String Artist", "String Genre", "String Artist", "String Genre"),
        ],
    )
    def test_combined_helpers(self, artists, genres, expected_artists, expected_genres):
        """Test both helpers together using parametrize."""
        artist_result = safe_artists(artists)
        genre_result = safe_genres(genres)

        assert artist_result == expected_artists
        assert genre_result == expected_genres
