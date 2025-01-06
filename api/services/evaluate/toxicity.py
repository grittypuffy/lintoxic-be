import asyncio
import logging


from api.services.processors.toxicity.classifier import ToxicContentClassifier, TamilToxicContentClassifier

toxic_content_classifier = ToxicContentClassifier.get_instance()
tamil_toxic_content_classifier = TamilToxicContentClassifier.get_instance()


async def check_toxicity(text: str):
    results = await asyncio.gather(
        asyncio.to_thread(toxic_content_classifier.predict, text),
        asyncio.to_thread(tamil_toxic_content_classifier.predict, text),
    )

    for result in results:
        if result.get("status"):
            return result

    return {"status": False, "reason": "The content provided does not have any toxic elements associated with it.", "labels": None}
