import os

from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("TELEGRAM_TOKEN")
ACCESS_KEY = os.getenv("ACRCLOUD_ACCESS_KEY")
ACCESS_SECRET = os.getenv("ACRCLOUD_SECRET_KEY")
