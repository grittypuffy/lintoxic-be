import aiohttp
import logging
from models.fact import FactCheckResponse
from config.constants import FACT_CHECKER_API_ENDPOINT as url
from config.constants import FACT_CHECKER_API_HEADERS as headers


async def check_fact_accuracy(text: str):
    data: dict = {
        "text": text
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                contents = await response.json()
                true_facts: int = 0
                false_contents: list[dict] = []
                for content in contents:
                    if content["is_correct"] == "True":
                        true_facts += 1
                    elif content["is_correct"] == "False":
                        false_contents.append(content)
                accuracy: float = 0.0
                if len(contents):
                    accuracy = (true_facts / len(contents)) * 100
                if false_contents:
                    return {"status": True, "accuracy": accuracy, "reason": "The provided content contains inaccurate information.", "false_content": false_contents}
                else:
                    return {"status": False, "accuracy": accuracy, "reason": "The provided content contains accurate information or is self-sufficient.", "false_content": None}

            else:
                raise Exception(f"{response.status}")
