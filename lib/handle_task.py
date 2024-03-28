import os
import requests
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin

logger = logging.getLogger()

AIDEVS_API_KEY = os.getenv("AI_DEVS_API_KEY")
AIDEVS_PREFIX = "https://tasks.aidevs.pl/"
URL_TOKEN_PREFIX = urljoin(AIDEVS_PREFIX, "token/")
URL_TASK_PREFIX = urljoin(AIDEVS_PREFIX, "task/")
URL_ANSWER_PREFIX = urljoin(AIDEVS_PREFIX, "answer/")
URL_HINT_PREFIX = urljoin(AIDEVS_PREFIX, "hint/")


def get_task_token(task_name: str) -> Optional[str]:
    """Get the task token for a particular task."""
    # Check if the AIDEVS_API_KEY is set in the environment
    if not AIDEVS_API_KEY:
        logger.error("Please set the AIDEVS_API_KEY environment variable")
        return None

    # Prepare parameters for token retrieval
    token_url = urljoin(URL_TOKEN_PREFIX, task_name)
    payload = {"apikey": AIDEVS_API_KEY}

    try:
        # Send request for token retrieval
        response = requests.post(url=token_url, json=payload)
        response_data = response.json()

        # Check response for success or failure
        if response_data["code"] == 0:
            logger.info("Token retrieval succeeded: %s", response_data["token"])
            return response_data["token"]
        else:
            logger.error("Token retrieval failed: %s", response_data.get("msg"))
            return None
    except ValueError as e:
        logger.error("Token retrieval failed: %s", e)


def get_task_details(token: str) -> Optional[Dict[str, Any]]:
    """Get task details using the ai_devs task token from previously registered authentication."""
    if not token:
        logger.error(
            "The ai_devs authentication token not found. Please ensure it is set."
        )
        return None

    # Construct URL for fetching task details
    task_url = urljoin(URL_TASK_PREFIX, token)

    try:
        # Send request for task retrieval
        response = requests.get(url=task_url)
        response_data = response.json()

        # Check response for success or failure
        if response_data["code"] == 0:
            logger.info("Task details retrieval succeeded: \n%s", response_data)
            return response_data
        else:
            logger.error("Task details retrieval failed: \n%s", response_data)
            return None
    except ValueError as e:
        logger.error("Task details retrieval failed: %s", e)
        return None


def send_answer(token, answer):
    """Send an answer for the task."""
    # Prepare the parameters for sending the task
    answer_url = urljoin(URL_ANSWER_PREFIX, token)
    payload = {"answer": answer}

    try:
        # Send the request for task submission
        response = requests.post(url=answer_url, json=payload)
        response_data = response.json()

        # Check if the request sending succeeded
        logger.info("Task answer sending succeeded: .\n%s", response_data)

        # Check if the answer submission succeeded (the answer is correct)
        if response_data["code"] == 0:
            logger.info("Task answer submission succeeded: \n%s", response_data)
            return response_data
        else:
            logger.error("Task answer submission failed: \n%s", response_data)
            return None
    except ValueError as e:
        logger.error("Task answer sending failed: \n%s", e)


def test_request(method, payload, is_json):
    """Test request using the httpbin."""
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
