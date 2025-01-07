import asyncio

from api.services.validate.text import evaluate_text
from api.utils.processor.video import VideoProcessor

video_processor = VideoProcessor.get_instance()


async def evaluate_video(path: str):
    result = await video_processor.process_video(path)
    if result.get("status"):
        return result

    return {"status": False, "reason": "The content provided does not have any toxic elements or inaccuracies associated with it.", "labels": None, "nsfw": False, "accuracy": False, "toxicity": False}
