import logging
import json

from openai_models import models
from openai import OpenAI

from lib.handle_task import (
    get_token,
    get_task_details,
    send_answer,
    test_request,
)

from lib.get_model import get_model

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get task details
token = get_token(task_name="blogger")
task = get_task_details(token=token)
outlines = task["blog"]

# Prepare messages for OpenAI
client = OpenAI()
model = get_model("gpt4")
messages = [
    {
        "role": "system",
        "content": """As a blogger assistant concisely provide blog post for a the provided outlines in the JSON format. The outlines format:
        ["outline 1", "outline 2", "outline 3", "outline 4"]

        Each outline should be transformed into a chapter of a blog post. Please do not include the outlines in the chapters. Each chapter should be in Polish. An answer should be returned as an array in the JSON format as following:
        ["chapter 1","chapter 2","chapter 3","chapter 4"]
        Do not return anything else apart from the JSON. Do not wrap the JSON.
        """,
    },
    {
        "role": "user",
        "content": f"""{outlines}""",
    },
]

# Call the Completions API to get blog post for given outlines
try:
    completion = client.chat.completions.create(
        model=model, messages=messages, temperature=0
    )

    # Dump the completion response to the python format
    response = completion.model_dump()

    logger.info(f"Successfully called the Completions API: {response}.\n")

    # Prepare an answer for the ai_devs
    answer = json.loads(response["choices"][0]["message"]["content"])
    url = f"https://tasks.aidevs.pl/answer/{token}"
    payload = {"answer": answer}

    # Test the request before sending
    test_request("POST", payload=payload)

    # Send the answer with a blog post to the ai_devs
    send_answer(token=token, answer=answer)

except Exception as e:
    logger.error(e)
