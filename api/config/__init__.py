from api.helpers.singleton import singleton
from motor.motor_asyncio import AsyncIOMotorDatabase
from api.config.environment import EnvVarConfig
from api.config.database import get_database
from api.config.celery import get_celery_instance


@singleton
class AppConfig():
    def __init__(self):
        self.env: EnvVarConfig = EnvVarConfig()
        self.db: AsyncIOMotorDatabase = get_database(self.env)
        self.celery = get_celery_instance()


def get_config():
    return AppConfig()
