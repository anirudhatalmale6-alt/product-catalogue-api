import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "change-me-in-production")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./products.db")
