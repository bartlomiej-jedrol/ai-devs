import logging
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


def get_gnome_hat_color(
    openai_client: OpenAI, model: str, image_url: str
) -> Optional[str]:
    """Get color of gnome hat using OpenAI model."""
    messages = []
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """Reply with only a color of gnome's hat and nothing else. Respond in Polish.
                    rules
                    - if the image does not show gnome - reply ERROR
                    """,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                },
            ],
        }
    )
    return create_completion(client=openai_client, model=model, messages=messages)


def main():
    """Send answer for ai_devs task."""
    ai_devs_task_token = get_task_token(task_name="gnome")
    image_url = get_task_details(token=ai_devs_task_token)["url"]

    openai_client = OpenAI()
    model = get_model("gpt4")

    # Get answer from OpenAI. Return None if there is no answer.
    answer = get_gnome_hat_color(
        openai_client=openai_client, model=model, image_url=image_url
    )
    if answer is None:
        return None

    # Send answer to te ai_devs server.
    send_answer(token=ai_devs_task_token, answer=answer)


main()
