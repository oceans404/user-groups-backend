from dotenv import load_dotenv
import os

load_dotenv()

# get .env variables
class Settings:
    PRIVY_APP_ID = os.getenv("PRIVY_APP_ID")
    PRIVY_APP_SECRET = os.getenv("PRIVY_APP_SECRET")
    PRIVY_JWKS_URL = os.getenv("PRIVY_JWKS_URL")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    MONGODB_URI = os.getenv("MONGODB_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")

settings = Settings()