import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Adicionar outras configurações aqui...

config = Config()