from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from api.helpers.singleton import singleton

load_dotenv()


@singleton
class EnvVarConfig(BaseSettings):
    environment: str
    cookie_domain: str
    api_domain: str
    frontend_url: str
    mongodb_uri: str
    mongodb_db: str
    upload_dir: str
    preprocessing_dir: str

    class EnvVarConfig:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_env_config():
    return EnvVarConfig()
