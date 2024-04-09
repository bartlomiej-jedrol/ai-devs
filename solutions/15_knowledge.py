import logging
import json
import requests
from typing import Optional, Tuple, Union, List, Dict

from openai import OpenAI
import pandas as pd

from lib.handle_task import get_task_token, get_task_details, send_answer
from lib.utilities import extract_urls, retrieve_json_data_from_url
from lib.get_model import get_model
from lib.openai_utilities import create_completion

logger = logging.getLogger()

OPENAI_CLIENT = OpenAI()
MODEL = get_model("gpt4")
EXCHANGE_RATE_FUNCTION_NAME = "get_exchange_rate"
COUNTRY_POPULATION_FUNCTION_NAME = "get_country_population"
OPENAI_FUNCTION_NAME = "get_openai_answer"


def get_function_specification():
    """Get the function specification for the determine service function."""
    return [
        {
            "type": "function",
            "function": {
                "name": "determine_service",
                "description": "determine function name based on user question",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "target_function_name": {
                            "type": "string",
                            "description": f"{EXCHANGE_RATE_FUNCTION_NAME}|{COUNTRY_POPULATION_FUNCTION_NAME}|{OPENAI_FUNCTION_NAME}",
                        },
                    },
                },
            },
        }
    ]


def determine_target_function_for_question(
    openai_client: OpenAI, model: str, question: str
) -> str:
    """Determine target function to be called for a given question.
    There are three services possible to be called and for each there is a separate function:
    - get_exchange_rate
    - get_country_population
    - get_openai_answer
    """
    messages = []
    messages.append(
        {
            "role": "system",
            "content": """Determine function name based on user question. There are three function to be chosen from:
                    - get_exchange_rate: only for questions related to exchanging rate
                    - get_country_population: only for questions related to population number
                    - get_openai_answer: rest of the questions
                    examples```
                    question: podaj aktualny kurs DOLARA
                    target_function_name: get_exchange_rate
                    question: jak nazywa się stolica Czech?
                    target_function_name: get_openai_answer
                    ```
                    """,
        }
    )
    messages.append({"role": "user", "content": question})
    tools = get_function_specification()

    arguments = create_completion(
        client=OPENAI_CLIENT, model=MODEL, messages=messages, tools=tools
    )
    return json.loads(arguments)["target_function_name"]


def get_exchange_rate(question: str):
    """Get exchange rate for currency."""
    table = "A"

    # Extract currency code from question
    messages = []
    messages.append(
        {
            "role": "system",
            "content": "Return only currency code in the ISO 4217 standard (three characters).",
        }
    )
    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )
    iso_currency_code = create_completion(
        client=OPENAI_CLIENT, model=MODEL, messages=messages
    )
    print(iso_currency_code)

    echange_rate_url = (
        f"http://api.nbp.pl/api/exchangerates/rates/{table}/{iso_currency_code}/today/"
    )
    response = requests.get(url=echange_rate_url)
    response_json = response.json()
    return response_json["rates"][0]["mid"]


def get_country_population(question: str):
    """Get country population for country."""

    # Extract country name from question
    messages = []
    messages.append(
        {
            "role": "system",
            "content": "Return only country name in English from question.",
        }
    )
    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )
    country_name = create_completion(
        client=OPENAI_CLIENT, model=MODEL, messages=messages
    )
    print(country_name)

    country_population_url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url=country_population_url)
    response_json = response.json()
    population = response_json[0]["population"]
    print(population)


def get_openai_answer(question: str):
    """Get answer for question."""
    messages = []
    messages.append(
        {
            "role": "system",
            "content": """Answer question very concisely.
                    examples```
                    question: Who wrote Romeo and Juliet?
                    response: William Shakespeare
                    ```
                    """,
        }
    )
    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )
    return create_completion(client=OPENAI_CLIENT, model=MODEL, messages=messages)


def extract_input_for_target_function(question: str) -> str:
    print("input")


def get_answer():
    """Get answer for a question from ai_devs."""
    ai_devs_task_token = get_task_token("knowledge")
    question = get_task_details(token=ai_devs_task_token)["question"]
    print(question)

    target_function = determine_target_function_for_question(
        openai_client=OPENAI_CLIENT, model=MODEL, question=question
    )

    if target_function == EXCHANGE_RATE_FUNCTION_NAME:
        answer = get_exchange_rate(question=question)
        print(answer)
    elif target_function == COUNTRY_POPULATION_FUNCTION_NAME:
        answer = get_country_population(question=question)
        print(answer)
    elif target_function == OPENAI_FUNCTION_NAME:
        answer = get_openai_answer(question=question)
        print(answer)

    print(send_answer(token=ai_devs_task_token, answer=answer))


get_answer()
