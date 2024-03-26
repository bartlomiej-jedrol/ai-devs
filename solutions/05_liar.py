import json
from lib.handle_task import (
    get_token,
    get_task,
    send_answer,
    test_request,
)
from lib.get_model import get_model
from openai import OpenAI
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

MODEL = get_model("gpt4")

# Get token
task_name = "liar"
token = get_token(task_name=task_name)

# Get task details
get_task(token=token)

# Set question
payload = {"question": "What is capital of Poland?"}

# Test request
# test_request(method="POST", payload=payload, is_json=False)

# Get an answer for the question from ai_devs
task_url = f"https://tasks.aidevs.pl/task/{token}"
response = requests.post(url=task_url, data=payload)
response_dict = response.json()
answer = response_dict["answer"]

# Verify if the answer answers the question
client = OpenAI()
messages = [
    {
        "role": "system",
        "content": """As an assistant you evaluate whether provided answer answers the provided question. Response format: YES/NO.

        ### Examples
        - question: What is capital of Poland?
        - answer: Warsaw
        - response: YES

        - question: What is the Content-Type for JSON?
        - answer: "application/x-www-form-urlencoded"
        - response: NO

        """,
    },
    {"role": "user", "content": f"question: {payload['question']}, answer: {answer}."},
]

try:
    # Create chat completions with specified model an messages
    completion = client.chat.completions.create(
        model=MODEL, messages=messages, temperature=0
    )

    # Dump the model data
    response = completion.model_dump()

    logger.info(f"Successfully called the Chat Completions API: {response}.\n")

except Exception as e:
    logger.error(e)

# print(json.dumps(response, indent=4))

# Send answer to ai_devs
task_answer = response["choices"][0]["message"]["content"]
send_answer(token=token, answer=task_answer)
