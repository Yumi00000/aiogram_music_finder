def safe_artists(artists_data) -> str:
    if isinstance(artists_data, list):
        return ", ".join([a.get("name", "Unknown Artist") for a in artists_data if isinstance(a, dict)])
    elif isinstance(artists_data, str):
        return artists_data
    return "Unknown Artist"


def safe_genres(genres_data) -> str:
    if isinstance(genres_data, list):
        return ", ".join([g.get("name", "Unknown Genre") for g in genres_data if isinstance(g, dict)])
    elif isinstance(genres_data, str):
        return genres_data
    return "Unknown Genre"
