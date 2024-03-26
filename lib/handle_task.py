# pylint: disable=all
import os
import requests
import logging

API_KEY = os.getenv("AI_DEVS_API_KEY")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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


def get_task(token):
    """Get task details."""
    url = f"https://tasks.aidevs.pl/task/{token}"
    try:
        r = requests.get(url=url)
        task = r.json()
        logger.info(f"Successfully obtained the task: {task}.\n")
        print(f"Successfully obtained the task: {task}.\n")
    except Exception as e:
        print(e)
        print("Error at the time of getting input data.\n")

    return r.json()


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
