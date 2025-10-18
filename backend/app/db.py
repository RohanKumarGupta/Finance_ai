import logging
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

client: AsyncIOMotorClient | None = None

def get_db():
    if client is None:
        raise RuntimeError("Mongo client not initialized")
    return client[settings.DATABASE_NAME]

async def connect_to_mongo():
    """Connect to MongoDB with error handling and verification."""
    global client
    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URI}")

        # Parse the connection string to check if database name is included
        parsed = urlparse(settings.MONGODB_URI)
        if parsed.path and parsed.path != '/':
            # Database name is already in the URI (e.g., /finance_db)
            actual_db_name = parsed.path.lstrip('/')
            logger.info(f"Database name found in URI: {actual_db_name}")
        else:
            actual_db_name = settings.DATABASE_NAME
            logger.info(f"Using database name from settings: {actual_db_name}")

        client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
        )

        # Test the connection
        await client.admin.command('ping')
        logger.info(f"Successfully connected to MongoDB database: {actual_db_name}")

    except ServerSelectionTimeoutError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise RuntimeError(f"Cannot connect to MongoDB server at {settings.MONGODB_URI}. Please check your connection string and network access.")
    except ConfigurationError as e:
        logger.error(f"MongoDB configuration error: {e}")
        raise RuntimeError(f"Invalid MongoDB configuration: {e}")
    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {e}")
        raise RuntimeError(f"Failed to connect to MongoDB: {e}")

async def close_mongo_connection():
    """Close MongoDB connection gracefully."""
    global client
    if client:
        logger.info("Closing MongoDB connection")
        client.close()
        client = None

async def check_mongo_connection():
    """Check if MongoDB connection is healthy."""
    try:
        db = get_db()
        ping_result = await db.command('ping')
        return ping_result.get('ok') == 1.0
    except Exception as e:
        logger.error(f"MongoDB health check failed: {e}")
        return False
