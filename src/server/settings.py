import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEBUG = bool(int(os.getenv("DEBUG", 0)))

