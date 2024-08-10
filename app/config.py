import os
from dotenv import load_dotenv

load_dotenv()
DATA_FOLDER = os.getenv("DATA_FOLDER")
DATABASE = os.getenv("DATABASE")