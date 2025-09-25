# Aiogram Music Finder

A Telegram bot based on aiogram for music recognition and search from audio messages.

## Features
- Recognize music from voice and audio messages
- Save user request history
- Provide information about found tracks
- Convenient menu and keyboard for interaction

## Requirements
- Python 3.12+
- PostgreSQL (or another supported database)
- ffmpeg (for audio conversion)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Yumi00000/aiogram_music_finder
   cd aiogram_music_finder
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables and settings in `bot/core/configure.py`.
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## Running
```bash
python main.py
```

## Project Structure
- `main.py` — entry point
- `bot/` — bot logic, handlers, services, keyboards
- `models/` — ORM models
- `schemas/` — serialization schemas
- `utils/` — helper functions
- `migrations/` — Alembic migrations
- `downloads/` — temporary audio files

## Usage
- Send an audio or voice message to the bot
- Receive track information
- View your request history

## Migrations & Database
- Alembic is used for migration management
- Models: User, Song, History

## Dependencies
- aiogram
- SQLAlchemy
- Alembic
- ffmpeg-python
- requests

## Contact
- Author: Yumi
- Telegram: [Yumi000000](https://t.me/Yumi000000)

---
For questions or suggestions, open an issue or contact directly.
