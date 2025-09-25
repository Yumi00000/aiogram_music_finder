from typing import Optional, Dict, Any
from pydantic import BaseModel

class SongSchema(BaseModel):
    title: str
    artist: Optional[str] = None
    album: Optional[str] = None
    release_date: Optional[str] = None
    genre: Optional[str] = None
    duration: Optional[int] = None
    links: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
