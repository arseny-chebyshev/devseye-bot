import os
import dotenv
dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_ENGINE = os.getenv('DB_ENGINE')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv('DB_PORT')
