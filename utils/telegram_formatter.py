from schemas.SongSchema import SongSchema
from models.song import SongModel

def format_song_for_telegram(song: SongSchema | SongModel | dict) -> str:
    if isinstance(song, dict):
        song = SongSchema(**song)
    elif isinstance(song, SongModel):
        song = SongSchema.from_orm(song)

    message = (
        f"🎵 *Title*: {song.title or 'Unknown'}\n"
        f"🎤 *Artists*: {song.artist or 'Unknown'}\n"
        f"💿 *Album*: {song.album or 'Unknown'}\n"
        f"📅 *Release Date*: {song.release_date or 'Unknown'}\n"
        f"🎼 *Genre*: {song.genre or 'Unknown'}\n"
    )

    if song.links:
        message += "\n🔗 *Links*:\n"
        if "deezer" in song.links:
            message += f"🎧 [Deezer]({song.links['deezer']})\n"
        if "spotify" in song.links:
            message += f"🎶 [Spotify]({song.links['spotify']})\n"
        if "youtube" in song.links:
            message += f"📺 [YouTube]({song.links['youtube']})\n"

    return message
