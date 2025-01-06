from api.helpers.singleton import singleton
from motor.motor_asyncio import AsyncIOMotorDatabase
from api.config.environment import EnvVarConfig
from api.config.database import get_database
from api.config.celery import get_celery_instance
from api.services.processors.nsfw.image import NSFWImageClassificationModel
from api.services.processors.audio import AudioProcessor
from api.services.processors.toxicity.classifier import ToxicContentClassifier, TamilToxicContentClassifier
from api.services.processors.video import VideoProcessor


@singleton
class AppConfig():
    def __init__(self):
        self.env: EnvVarConfig = EnvVarConfig()
        self.db: AsyncIOMotorDatabase = get_database(self.env)
        self.celery = get_celery_instance()
        self.toxic_content_classifier = ToxicContentClassifier.get_instance()
        self.tamil_toxic_content_classifier = TamilToxicContentClassifier.get_instance()
        self.nsfw_image_classifier = NSFWImageClassificationModel.get_instance()
        self.audio_processor = AudioProcessor.get_instance()
        self.video_processor = VideoProcessor.get_instance()


def get_config():
    return AppConfig()
