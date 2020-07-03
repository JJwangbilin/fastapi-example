import logging
import sys
from typing import List
from databases import DatabaseURL
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from app.core.logging import InterceptHandler

API_PREFIX = "/api"

JWT_TOKEN_PREFIX = "Token"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
VERSION = "0.0.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=True)
HOST: str = config("HOST", default='0.0.0.0')
PORT: int = config("PORT", cast=int, default=8080)
# mongo
MONGODB_URL: DatabaseURL = config("MONGODB_URL", cast=DatabaseURL, default='mongodb://127.0.0.1:27017')
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
# redis
REDIS_HOST: str = config("REDIS_HOST", cast=str, default='127.0.0.1')
REDIS_PORT: int = config("REDIS_PORT", cast=int, default=6379)
REDIS_PASSWD: str = config("REDIS_PASSWD", cast=str, default='')

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default='welcome1')

PROJECT_NAME: str = config("PROJECT_NAME", default="FastAPI example")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="",
)
# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]
# sink可自主配置
logger.configure(
    handlers=[{"sink": sys.stdout, "level": LOGGING_LEVEL}, {"sink": './runtime.log', "level": LOGGING_LEVEL}])
# mongo db info
database_name: str = config('DATABASE_NAME', default='moop')
user_collection_name = 'user'
