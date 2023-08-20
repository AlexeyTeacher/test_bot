import os
import logging
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TKN')
DB_USER = os.getenv('DB_USER')
DB_PWD = os.getenv('DB_PWD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_SCHEMA = 'practicum'
DB_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

OWNER_NAME = os.getenv('OWNER_NAME')
OWNER_LOGIN = os.getenv('OWNER_LOGIN')

# Этапы/состояния разговора
FIRST, LAST_SELFIE_END, SCHOOL_PHOTO_END, STORY_END, GPT_END, BASES_END, FIRST_LOVE_END, DOWNLOAD_START, DOWNLOAD_END = range(9)
# Данные обратного вызова
LAST_SELFIE_START, SCHOOL_PHOTO_START, STORY_START, GPT_START, BASES_START, FIRST_LOVE_START, END, HELP = range(8)

LOG_FORMAT = '[%(levelname) -3s %(asctime)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)
