from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from app.db.mongodb import db


async def connect_to_mongodb() -> None:
    logger.info("连接数据库中...")
    db.client = AsyncIOMotorClient(str(MONGODB_URL),
                                   maxPoolSize=MAX_CONNECTIONS_COUNT,
                                   minPoolSize=MIN_CONNECTIONS_COUNT)
    logger.info("连接数据库成功！")


async def close_mongo_connection():
    logger.info("关闭数据库连接...")
    db.client.close()
    logger.info("数据库连接关闭！")
