"""
Configuration loader for IoT Home Security System
Loads from .env file in development or environment variables in production (Render)
"""

from os import getenv
from pathlib import Path
from dotenv import load_dotenv

# Load local .env when present (safe: on Render, system environment variables are used)
_dotenv = Path(__file__).parent / '.env'
if _dotenv.exists():
    load_dotenv(dotenv_path=_dotenv)

# Adafruit IO Configuration
AIO_USERNAME = getenv('AIO_USERNAME')
AIO_KEY = getenv('AIO_KEY')

# Database Configuration
DATABASE_URL = getenv('DATABASE_URL')

# Flask Configuration
FLASK_SECRET_KEY = getenv('FLASK_SECRET_KEY', 'change-me-in-production')

# Raspberry Pi Configuration (if needed for remote connections)
RSPI_HOST = getenv('RSPI_HOST')
RSPI_PORT = int(getenv('RSPI_PORT', '22'))
RSPI_USER = getenv('RSPI_USER')
RSPI_PASSWORD = getenv('RSPI_PASSWORD')
RSPI_SSH_KEY_PATH = getenv('RSPI_SSH_KEY_PATH')

# Feed names - using environment variables with fallback to defaults
FEED_TEMPERATURE = getenv('FEED_TEMPERATURE', 'temperature')
FEED_HUMIDITY = getenv('FEED_HUMIDITY', 'humidity')
FEED_MOTION = getenv('FEED_MOTION', 'motion-state')
FEED_LIGHT = getenv('FEED_LIGHT', 'light-level')
FEED_FAN = getenv('FEED_FAN', 'fan-toggle')
FEED_MODE = getenv('FEED_MODE', 'system-mode')
FEED_CAMERA = getenv('FEED_CAMERA', 'camera-last-image-timestamp')

# Build full feed paths
def get_feed_path(feed_name):
    """Get full Adafruit IO feed path"""
    if AIO_USERNAME:
        return f'{AIO_USERNAME}/feeds/{feed_name}'
    return feed_name

FEEDS = {
    'temperature': get_feed_path(FEED_TEMPERATURE),
    'humidity': get_feed_path(FEED_HUMIDITY),
    'motion': get_feed_path(FEED_MOTION),
    'light': get_feed_path(FEED_LIGHT),
    'fan': get_feed_path(FEED_FAN),
    'mode': get_feed_path(FEED_MODE),
    'camera': get_feed_path(FEED_CAMERA)
}

