import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from urllib.parse import urljoin

from openai import OpenAI

from lib.handle_task import get_task_token, get_task_details, send_answer
from lib.utilities import send_request
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

OPENAI_CLIENT = OpenAI()
MODEL = get_model("gpt4")
CURRENCY = "currency"
COUNTRY = "country"
ANSWER = "answer"


def get_function_specification():
    """Get the function specification for the determine service function (Function calling)."""
    return [
        {
            "type": "function",
            "function": {
                "name": "determine_service",
                "description": "Determine function name and its input based on user question.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "Unchanged user question.",
                        },
                        "service_name": {
                            "type": "string",
                            "description": f"{CURRENCY} (only for questions related to exchanging rate) | {COUNTRY} (only for questions related to population number) | {ANSWER} (otherwise)",
                            "enum": [CURRENCY, COUNTRY, ANSWER],
                        },
                        CURRENCY: {
                            "type": "string",
                            "description": "Currency code in the ISO 4217 standard (three characters)",
                        },
                        COUNTRY: {
                            "type": "string",
                            "description": "Country name in English",
                        },
                        ANSWER: {
                            "type": "string",
                            "description": "Answer for user question. Required in service_name is answer.",
                        },
                    },
                    "required": ["question", "service_name"],
                },
            },
        }
    ]


def classify_question(openai_client: str, model: str, question: str) -> Dict[str, Any]:
    """Classify question using OpenAI model.
    Return arguments.
    """
    messages = []
    messages.append({"role": "system", "content": ""})
    messages.append({"role": "user", "content": question})
    tools = get_function_specification()
    arguments = create_completion(
        client=openai_client, model=model, messages=messages, tools=tools
    )
    return json.loads(arguments)


def execute_target_function(arguments: Dict[str, str]) -> Optional[Any]:
    """
    Map service name to target function.
    Execute target function based on provided arguments from the OpeAI model.
    Return answer based on the target function execution.

    Mapping:
    - service name -> target function
    - currency -> get_exchange_rate
    - country -> get_country_population
    - answer -> get_openai_answer
    """
    service_name = arguments.get("service_name")
    if service_name == CURRENCY:
        function_input = arguments[CURRENCY]
        answer = get_exchange_rate(function_input=function_input)
    elif service_name == COUNTRY:
        function_input = arguments[COUNTRY]
        answer = get_country_population(function_input=function_input)
    elif service_name == ANSWER:
        answer = arguments[ANSWER]

    if answer is not None:
        return answer


def get_exchange_rate(function_input: str) -> Optional[float]:
    """Get exchange rate for currency."""
    base_url = "http://api.nbp.pl/api/exchangerates/tables/"
    table = "A"
    previous_day_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    exchange_rate_url = urljoin(base_url, f"{table}/{previous_day_date}/")

    # Send a request to the NBP API
    response_json = send_request(url=exchange_rate_url)
    if response_json is None:
        return None

    currency_rate = None
    for rate in response_json[0]["rates"]:
        if rate["code"] == function_input:
            currency_rate = rate["mid"]
            break
    return currency_rate


def get_country_population(function_input: str) -> Optional[int]:
    """Get country population for country."""
    base_url = "https://restcountries.com/v3.1/name/"
    country_population_url = urljoin(base_url, function_input)

    # Send request to the country population api
    response_json = send_request(url=country_population_url)
    if response_json is None:
        return None

    return response_json[0]["population"]


def main() -> None:
    """Get answer for the ai_devs question."""
    ai_devs_task_token = get_task_token("knowledge")
    question = get_task_details(token=ai_devs_task_token)["question"]

    arguments = classify_question(
        openai_client=OPENAI_CLIENT, model=MODEL, question=question
    )
    if arguments is None:
        return None

    answer = execute_target_function(arguments=arguments)
    if answer is None:
        return None

    # Send answer to ai_devs server
    send_answer(token=ai_devs_task_token, answer=answer)


main()
