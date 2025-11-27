import os
import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)

client: Optional[AsyncIOMotorClient] = None
db = None


async def connect_to_mongo(app):

    global client, db
    uri = os.getenv("MONGODB_URI") or os.getenv("MONGODB_URI_LOCAL")
    if not uri:
        logger.warning("No MongoDB URI found in environment; skipping DB connection.")
        return

    logger.info("Connecting to MongoDB...")
    client = AsyncIOMotorClient(uri)

    try:
        database = client.get_default_database()
    except Exception:
        # Fallback DB name — adjust if you use a different database name
        database = client.get_database("adeybloom")

    db = database
    app.state.mongo_client = client
    app.state.db = db
    logger.info("MongoDB connection established")


async def close_mongo(app):
    global client
    if client:
        logger.info("Closing MongoDB connection...")
        client.close()
        client = None
        logger.info("MongoDB connection closed")



