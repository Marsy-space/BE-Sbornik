from loguru import logger
import sys
import os

os.makedirs("logs", exist_ok=True)

logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/app.log", rotation="10 MB", retention="7 days", level="DEBUG")

def get_logger():
    return logger
