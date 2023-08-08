import os
from dotenv import load_dotenv

load_dotenv()

VERSION = "0.1.0"
UPTIME_KUMA_URL = os.getenv("UPTIME_KUMA_URL")
UPTIME_KUMA_USERNAME = os.getenv("UPTIME_KUMA_USERNAME")
UPTIME_KUMA_PASSWORD = os.getenv("UPTIME_KUMA_PASSWORD")
