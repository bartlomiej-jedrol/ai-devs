import logging
import json
from typing import Optional, Dict
from datetime import datetime

from openai import OpenAI

from lib.handle_task import get_task_token, get_task_details, send_answer
from lib.get_model import get_model
from lib.openai_utilities import create_completion

logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)
logger = logging.getLogger()


def classify_task(
    openai_client: str, model: str, task: str
) -> Optional[Dict[str, str]]:
    """Classify task with use of OpenAI model:
    - ToDo
    - Calendar
    """
    messages = []
    messages.append(
        {
            "role": "system",
            "content": f"""Classify a task.
            Respond with a JSON object. tool (ToDo|Calendar), desc, date in format YYYY-MM-DD (only for Calendar)
            facts
            - today is: {datetime.now().strftime("%Y-%m-%d")}
            rules
            - if there is no deadline - does not include date
            """,
        }
    )
    messages.append({"role": "user", "content": task})

    return create_completion(
        client=openai_client,
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
    )


def main():
    """Send answer for ai_devs task."""
    ai_devs_task_token = get_task_token(task_name="tools")
    task = get_task_details(token=ai_devs_task_token)["question"]
    logger.info(f"ai_devs task: {task}")

    openai_client = OpenAI()
    model = get_model("gpt4")

    # Classify task received from ai_devs using OpenAI model
    answer = classify_task(openai_client=openai_client, model=model, task=task)
    answer_json = json.loads(answer)
    logger.info(f"OpenAI response: {answer}")

    # Send answer to ai_devs
    send_answer(token=ai_devs_task_token, answer=answer_json)


main()
