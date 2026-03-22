import os
from dotenv import load_dotenv

load_dotenv()

APPLICATION_ID = os.getenv("APPLICATION_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

SITE_HOSTNAME = os.getenv("SITE_HOSTNAME")
SITE_PATH = os.getenv("SITE_PATH")

DATABASE_URL = os.getenv("DATABASE_URL")