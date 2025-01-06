import asyncio

from api.services.processors.nsfw.image import NSFWImageClassificationModel
from api.services.processors.image import extract_text
from api.services.validate.text import evaluate_text

nsfw_image_classifier = NSFWImageClassificationModel.get_instance()


async def evaluate_image(path: str):
    text = extract_text(path)

    if text:
        result = await evaluate_text(text)
        if result.get("status"):
            return result

    nsfw_result = nsfw_image_classifier.predict(path)

    if nsfw_result.get("status"):
        return nsfw_result

    return {"status": False, "reason": "The content provided does not have any toxic elements, NSFW content or inaccuracies associated with it.", "labels": None, "nsfw": False, "accuracy": False, "toxicity": False}
