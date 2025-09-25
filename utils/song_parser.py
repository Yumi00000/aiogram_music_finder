from typing import Dict, Any
from utils.helpers import safe_artists, safe_genres

def parse_song(acr_song: Dict[str, Any]) -> Dict[str, Any]:
    song_info = {
        "title": acr_song.get("title", "Unknown Title"),
        "artists": safe_artists(acr_song.get("artists")),
        "album": acr_song.get("album", {}).get("name", "Unknown Album") if isinstance(acr_song.get("album"), dict) else acr_song.get("album"),
        "release_date": acr_song.get("release_date", "Unknown Date"),
        "duration_ms": acr_song.get("duration_ms"),
        "genres": safe_genres(acr_song.get("genres")),
        "acrid": acr_song.get("acrid"),
        "links": {},
    }

    external_metadata = acr_song.get("external_metadata", {})
    if "deezer" in external_metadata:
        song_info["links"]["deezer"] = f"https://www.deezer.com/track/{external_metadata['deezer']['track']['id']}"
    if "spotify" in external_metadata:
        song_info["links"]["spotify"] = f"https://open.spotify.com/track/{external_metadata['spotify']['track']['id']}"
    if "youtube" in external_metadata:
        song_info["links"]["youtube"] = f"https://www.youtube.com/watch?v={external_metadata['youtube']['vid']}"

    return song_info
