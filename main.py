import os
import requests
import logging

API_KEY = os.getenv("AI_DEVS_API_KEY")
task_name = "helloapi"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def authorize(task_name):
    """Authorize"""
    authorization_url = f"https://tasks.aidevs.pl/token/{task_name}"
    payload = {"apikey": API_KEY}
    try:
        r = requests.post(url=authorization_url, json=payload)
        logger.info(f"Successfully authorized the task: {task_name}.")
    except Exception as e:
        print(e)
        print(f"Error at the time of authorization of the task: {task_name}.")
        raise e

    return r.json()["token"]


def get_input_data(token):
    """Get task details"""
    task_url = f"https://tasks.aidevs.pl/task/{token}"
    try:
        r = requests.get(task_url)
        logger.info("Successfully obtained the input data.")
    except Exception as e:
        print(e)
        print("Error at the time of getting input data.")

    return r.json()["cookie"]


def send_answer(answer):
    "Send response"
    answer_url = f"https://tasks.aidevs.pl/answer/{token}"
    payload = {"answer": answer}
    try:
        r = requests.post(url=answer_url, json=payload)
        logger.info("Successfully sent the answer.")
    except Exception as e:
        print(e)
        print("Error at the time of sending answer.")
    return r


token = authorize(task_name=task_name)
answer = get_input_data(token=token)
response = send_answer(answer=answer)
print(response.json())
