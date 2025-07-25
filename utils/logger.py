import logging
import os
from logging.handlers import RotatingFileHandler

# Ensure log directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "agent_system.log")

# Configure log rotation: 5 MB per file, keep 3 backups
handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)

# Set log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)

# Set up logger
logger = logging.getLogger("AgentSystem")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
