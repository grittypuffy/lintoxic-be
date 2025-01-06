import asyncio
import logging


from api.services.processors.toxicity.classifier import ToxicContentClassifier, TamilToxicContentClassifier
from api.config import AppConfig, get_config

config: AppConfig = get_config()


async def check_toxicity(text: str):
    results = await asyncio.gather(
        asyncio.to_thread(config.toxic_content_classifier.predict, text),
        asyncio.to_thread(config.tamil_toxic_content_classifier.predict, text),
    )

    for result in results:
        if result.get("status"):
            return result

    return {"status": False, "reason": "The content provided does not have any toxic elements associated with it.", "labels": None}
