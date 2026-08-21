import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8969356827:AAF5hb41JUta2kuQOzd5LbEPxMp7aCKmATU")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "7807771944").split(",") if x]
DB_URL = "sqlite+aiosqlite:///bot/database.db"
