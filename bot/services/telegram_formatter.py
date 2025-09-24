from typing import Dict

def format_song_for_telegram(song_info: Dict) -> str:
    message = (
        f"🎵 *Title*: {song_info['title']}\n"
        f"🎤 *Artists*: {song_info['artists']}\n"
        f"💿 *Album*: {song_info['album']}\n"
        f"📅 *Release Date*: {song_info['release_date']}\n"
        f"🎼 *Genre*: {song_info['genres']}\n"
    )

    links = song_info.get("links", {})
    if links:
        message += "\n🔗 *Links*:\n"
        if "deezer" in links:
            message += f"🎧 [Deezer]({links['deezer']})\n"
        if "spotify" in links:
            message += f"🎶 [Spotify]({links['spotify']})\n"
        if "youtube" in links:
            message += f"📺 [YouTube]({links['youtube']})\n"

    return message
