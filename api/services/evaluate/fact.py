import aiohttp
import logging
from api.models.fact import FactCheckResponse
from api.constants import FACT_CHECKER_API_ENDPOINT as url
from api.constants import FACT_CHECKER_API_HEADERS as headers


async def check_fact_accuracy(text: str):
    i = 0
    text_content = text.split(" ")
    true_facts: int = 0
    false_contents: list[dict] = []
    accuracy: float = 0.0
    length = 0
    while text_content[i:i+125]:
        data: dict = {
            "text": text
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    contents = await response.json()
                    for content in contents:
                        if content["is_correct"] == "True":
                            true_facts += 1
                        elif content["is_correct"] == "False":
                            false_contents.append(content)
                        length += 1
                    if length:
                        accuracy = (true_facts / length) * 100

                else:
                    raise Exception(f"{response.status}")
        i += 125
    if false_contents:
        return {"status": True, "score": accuracy, "reason": f"The provided content contains inaccurate information. {false_contents[0].get("explanations")}", "false_content": false_contents, "accuracy": True}
    else:
        return {"status": False, "score": accuracy, "reason": "The provided content contains accurate information or is self-sufficient.", "false_content": None, "accuracy": False}
