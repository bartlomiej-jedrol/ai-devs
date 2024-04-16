import requests
import os
import json
import logging
from typing import Dict, List

from openai import OpenAI
from lib.handle_task import get_task_token, get_task_details, send_answer
from lib.openai_utilities import create_completion
from lib.get_model import get_model

logger = logging.getLogger(__name__)
OPENAI_CLIENT = OpenAI()
AI_DEVS_TASK_NAME = "optimaldb"


def get_database_source_file() -> Dict[str, List[str]]:
    """Get database from the ai_devs server."""
    ai_devs_task_token = get_task_token(task_name=AI_DEVS_TASK_NAME)

    # Get database URL
    database_url = get_task_details(token=ai_devs_task_token)["database"]

    # Get database JSON file
    try:
        response = requests.get(url=database_url)
        response.raise_for_status()
        database = response.json()

        # Save the database JSON file
        try:
            with open("database.json", "w") as f:
                json.dump(database, f)
        except Exception as e:
            logger.error(f"Failed to save the database file: {e}")
    except Exception as e:
        logger.error(f"Failed to request the database file: {e}")

    # Check size of the database file
    file_size = os.path.getsize("database.json")
    print(file_size)
    return database


def summarize_person_information(database: Dict[str, str], context: str = None) -> str:
    """Summarize information about all persons in the database."""
    all_person_descriptions = ""

    # If context is None, set it to an empty string
    if context == None:
        context = ""

    # Loop through the database and summarize information about each person
    for _, statements in database.items():
        person_description = "\n".join(statements)

        # Create a list of messages to send to the AI model for summarization
        messages = []
        messages.append(
            {
                "role": "system",
                "content": f"""Carefully summarize the provided message, ensuring that all details are retained, particularly any information pertaining to individuals involved. Aim to consolidate information for conciseness but without excluding any content. Double-check your summary before responding to confirm that no critical details are missing. In the summarization, also include information from the message about the context.
                ```context
                {context}
                ```
                """,
            }
        )
        messages.append(
            {
                "role": "user",
                "content": f"{person_description}",
            }
        )

        # Get the shortened person description
        person_description_shortened = create_completion(
            client=OPENAI_CLIENT, model=get_model("gpt4"), messages=messages
        )

        # Append the shortened person description to the all_person_descriptions string
        all_person_descriptions += f"{person_description_shortened}\n\n"

        # Check size of the string content in bytes
        # content_size = len(all_person_descriptions.encode("utf-8"))
        # print(f"The size of the string content is {content_size} bytes.")
    print(all_person_descriptions)
    return all_person_descriptions


def main():
    """Send answer for ai_devs task."""
    database = get_database_source_file()

    with open("database.json", "r") as f:
        database = json.load(f)

    all_person_descriptions = summarize_person_information(database=database)

    # Send an initial answer to the AI Devs task
    ai_devs_task_token = get_task_token(task_name=AI_DEVS_TASK_NAME)
    ai_devs_response = send_answer(
        token=ai_devs_task_token, answer=all_person_descriptions
    )

    # If the response code is -99, enrich the user message with missing context
    while ai_devs_response["code"] == -99:
        message = ai_devs_response["msg"]

        #
        messages = []
        messages.append(
            {
                "role": "system",
                "content": """From the user message extract what information is missing. Format response: missing information.
                ```examples:
                U: Can't find info about favourite Zygfryd movie
                S: ulubiony film Zygfryda
                ```
                """,
            }
        )
        messages.append(
            {
                "role": "user",
                "content": f"{message}",
            }
        )

        # Get the missing context
        missing_context = create_completion(
            client=OPENAI_CLIENT, model=get_model("gpt4"), messages=messages
        )
        print(f"\n{missing_context}\n")

        # Summarize information about all persons in the database with the missing context
        all_person_descriptions = summarize_person_information(
            database=database, context=missing_context
        )

        # Send the answer enriched with the missing context to the AI Devs task
        ai_devs_task_token = get_task_token(task_name=AI_DEVS_TASK_NAME)
        ai_devs_response = send_answer(
            token=ai_devs_task_token, answer=all_person_descriptions
        )


main()
