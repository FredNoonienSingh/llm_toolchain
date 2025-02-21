"""common things in the toolchain """
from loguru import logger

logger.add("logs/logs.log", level="INFO", format="{time} {level} {message}")
