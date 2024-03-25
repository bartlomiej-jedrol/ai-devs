from lib.handle_task import get_token, get_task, send_answer
from openai_models import models
from openai import OpenAI
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get token
task_name = "blogger"
token = get_token(task_name=task_name)

# Get task details
task = get_task(token=token)
outlines = task["blog"]

# Call the OpenAI completion API.
client = OpenAI()
model = models["gpt4"]
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

try:
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=0
    ).model_dump()
    logger.info(f"Successfully called the Completions API: {response}.\n")
except Exception as e:
    print(e)

# The task is to to POST a blog post for a given outline
answer = json.loads(response["choices"][0]["message"]["content"])
send_answer(token=token, answer=answer)
