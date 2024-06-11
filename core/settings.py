# settings.py
from decouple import config
from dotenv import load_dotenv

from decouple import config


load_dotenv()  # Load environment variables from.env file


# MongoDB connection settings
MONGO_HOST = config('MONGO_HOST')
MONGO_PORT = config('MONGO_PORT', cast=int)
MONGO_DB = config('MONGO_DB')
MONGO_COLLECTION = config('MONGO_COLLECTION')

# Telegram bot token
BOT_TOKEN = config('BOT_TOKEN')
