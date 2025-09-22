from __future__ import annotations
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    bot_token: str = os.getenv("BOT_TOKEN", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./salesbot.db")

<<<<<<< HEAD
settings = Settings()
=======
settings = Settings()
>>>>>>> d26e15bb748e2dacfacaec01384eaf20197cfb35
