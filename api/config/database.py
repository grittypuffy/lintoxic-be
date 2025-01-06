from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Depends
from api.config.environment import EnvVarConfig, get_env_config


def get_database(config: EnvVarConfig) -> AsyncIOMotorDatabase:
    client: AsyncIOMotorClient = AsyncIOMotorClient(config.mongodb_uri)
    database: AsyncIOMotorDatabase = client[config.mongodb_db]
    return database
