import asyncio

from api.services.validate.text import evaluate_text
from api.config import AppConfig, get_config

config: AppConfig = get_config()


async def evaluate_audio(path: str):
    transcription = config.audio_processor.process_audio(path)

    if (text := transcription.get("transcription")):
        result = await evaluate_text(text)
        if result.get("status"):
            return result

    return {"status": False, "reason": "The content provided does not have any toxic elements or inaccuracies associated with it.", "labels": None, "nsfw": False, "accuracy": False, "toxicity": False}
