import asyncio

from api.services.validate.text import evaluate_text
from api.services.processors.audio import AudioProcessor

audio_processor = AudioProcessor.get_instance()


async def evaluate_audio(path: str):
    transcription = audio_processor.process_audio(path)

    if (text := transcription.get("transcription")):
        result = await evaluate_text(text)
        if result.get("status"):
            return result

    return {"status": False, "reason": "The content provided does not have any toxic elements or inaccuracies associated with it.", "labels": None, "nsfw": False, "accuracy": False, "toxicity": False}
