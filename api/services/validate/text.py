import asyncio
from api.services.evaluate.toxicity import check_toxicity
from api.services.evaluate.fact import check_fact_accuracy


async def evaluate_text(text: str):
    results = await asyncio.gather(
        check_toxicity(text),
        check_fact_accuracy(text)
    )

    for result in results:
        if result.get("status"):
            return result

    return {"status": False, "reason": "The content provided does not have any toxic elements or inaccuracies associated with it.", "labels": None, "nsfw": False, "accuracy": False, "toxicity": False}
