# pylint: disable=all
import os
import requests
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin

API_KEY = os.getenv("AI_DEVS_API_KEY")

logger = logging.getLogger()

AIDEVS_PREFIX = "https://tasks.aidevs.pl/"
URL_TOKEN_PREFIX = urljoin(AIDEVS_PREFIX, "token/")
URL_TASK_PREFIX = urljoin(AIDEVS_PREFIX, "task/")
URL_ANSWER_PREFIX = urljoin(AIDEVS_PREFIX, "answer/")
URL_HINT_PREFIX = urljoin(AIDEVS_PREFIX, "hint/")


def get_token(task_name):
    """Get token for a task."""
    url = f"https://tasks.aidevs.pl/token/{task_name}"
    payload = {"apikey": API_KEY}
    try:
        r = requests.post(url=url, json=payload)
        logger.info(f"Successfully authorized the task: {task_name}.")
        print(f"Successfully authorized the task: {task_name}.\n")
    except Exception as e:
        print(e)
        print(f"Error at the time of authorization of the task: {task_name}.\n")
        raise e

    return r.json()["token"]


def get_task_details(token: str) -> Optional[Dict[str, Any]]:
    """Get task details using the ai_devs authentication token from previously registered authentication."""
    if not token:
        logger.error(
            "The ai_devs authentication token not found. Please ensure it is set."
        )
        return None

    # Construct URL for fetching task details
    task_url = urljoin(URL_TASK_PREFIX, token)

    logger.debug("Task URL: %s", task_url)

    try:
        response = requests.get(url=task_url)
        response_data = response.json()
        if response_data["code"] == 0:
            logger.info("Success response: \n\t%s\n", response_data)
            return response_data
        else:
            logger.error("Error response: ", response_data)
            return None

    except ValueError as e:
        logger.error("Error response: ", e)
        return None


def prepare_request(method, url, body):
    # Prepare your request
    req = requests.Request(method=method, url=url, json=body)
    prepared = req.prepare()

    # Print out the request's method and url
    print(
        "{}\n{}\n{},\n\n{}\n{}".format(
            "-----------START-----------",
            prepared.method + " " + prepared.url,
            "\n".join("{}: {}".format(k, v) for k, v in prepared.headers.items()),
            prepared.body,
            "-----------END-----------",
        )
    )


def test_request(method, payload, is_json):
    if method == "GET" and is_json:
        url = "https://httpbin.org/get"
        response = requests.get(url=url, json=payload)
    elif method == "GET" and not is_json:
        url = "https://httpbin.org/get"
        response = requests.get(url=url, data=payload)
    elif method == "POST" and is_json:
        url = "https://httpbin.org/post"
        response = requests.post(url=url, json=payload)
    elif method == "POST" and not is_json:
        url = "https://httpbin.org/post"
        response = requests.post(url=url, data=payload)

    print(response.text)


def send_answer(token, answer):
    "Send an answer to the task."
    answer_url = f"https://tasks.aidevs.pl/answer/{token}"
    payload = {"answer": answer}
    try:
        r = requests.post(url=answer_url, json=payload)
        logger.info(f"Successfully sent the answer: {payload}.\n")
        print(f"Successfully sent the answer: {payload}.\n")
    except Exception as e:
        print(e)
        print("Error at the time of sending answer.\n")
    print(f"Response from the answer endpoint: {r}.\n")
    # print(f"Response from the answer endpoint: {r.status_code}.\n")
    # print(f"Response from the answer endpoint: {r.headers}.\n")
    # print(f"Response from the answer endpoint: {r.ok}.\n")
    # print(f"Response from the answer endpoint: {r.text}.\n")
