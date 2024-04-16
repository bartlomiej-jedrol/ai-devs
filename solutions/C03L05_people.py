import logging
from typing import Optional, Tuple, Union, List, Dict

from openai import OpenAI
import pandas as pd

from lib.handle_task import get_task_token, get_task_details, send_answer
from lib.utilities import extract_urls, retrieve_json_data_from_url
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


def retrieve_input_from_task(task_name: str) -> Tuple[str, str, str]:
    """Retrieve question and JSON url from ai_devs server."""
    ai_devs_task_name = task_name
    ai_devs_task_token = get_task_token(task_name=ai_devs_task_name)
    task_details_response = get_task_details(token=ai_devs_task_token)
    question = task_details_response["question"]
    json_url = extract_urls(text=task_details_response["data"])
    return question, json_url, ai_devs_task_token


def extract_person_from_question(
    openai_client: OpenAI, model: str, question: str
) -> Optional[Tuple[str, str]]:
    """Extract person data from question using OpenAI's Chat completion API."""
    messages = []
    messages.append(
        {
            "role": "system",
            "content": f"""Return only name and surname of the person separated by ; character.
                    Examples```
                    user: Ulubiona potrawa Jana Kowalskiego to?
                    assistant: Jan;Kowalski
                    ```
                    """,
        }
    )
    messages.append({"role": "user", "content": question})
    content = create_completion(client=openai_client, model=model, messages=messages)
    return content.split(";")[0], content.split(";")[1] if content is not None else None


def query_person_from_json(
    json_data: List[Dict[str, str]], name: str, surname: str
) -> Optional[Dict[str, str]]:
    """Query person data from JSON."""
    df = pd.DataFrame(json_data)
    filtered_df = df[(df["imie"] == name) & (df["nazwisko"] == surname)]
    return filtered_df.to_dict(orient="records") if not filtered_df.empty else None


def answer_question(
    openai_client: OpenAI,
    model: str,
    question: str,
    person_data: Dict[str, Union[str, int]],
):
    """Answer question from ai_devs using person data."""
    messages = []
    messages.append(
        {
            "role": "system",
            "content": f"""Answer question using context.
                     Context```
                     {person_data}
                     ```
                     """,
        }
    )
    messages.append({"role": "user", "content": question})
    content = create_completion(client=openai_client, model=model, messages=messages)
    return content if content is not None else None


def get_answer():
    """Get answer for the question from the ai_devs."""
    question, json_url, ai_devs_task_token = retrieve_input_from_task("people")

    # Extract person the question is about
    openai_client = OpenAI()
    model = get_model("gpt4")
    person = extract_person_from_question(
        openai_client=openai_client, model=model, question=question
    )
    if person is None:
        return None

    # Retrieve JSON with persons data
    json_data = retrieve_json_data_from_url(json_url=json_url)
    if json_data is None:
        return None

    # Filter person data
    name, surname = person
    person_data = query_person_from_json(
        json_data=json_data, name=name, surname=surname
    )
    if person_data is None:
        return None

    # Answer question about the person using filtered person data
    answer = answer_question(
        openai_client=openai_client,
        model=model,
        question=question,
        person_data=person_data,
    )
    if answer is None:
        return None

    # Send answer to the ai_devs
    send_answer(token=ai_devs_task_token, answer=answer)


get_answer()
