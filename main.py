import os
import requests

API_KEY = os.getenv("AI_DEVS_API_KEY")
task_name = "helloapi"


def authorize(task_name):
    """Authorize"""
    authorization_url = f"https://tasks.aidevs.pl/token/{task_name}"
    payload = {"apikey": API_KEY}
    r = requests.post(url=authorization_url, json=payload)
    return r.json()["token"]


def get_input_data(token):
    """Get task details"""
    task_url = f"https://tasks.aidevs.pl/task/{token}"
    r = requests.get(task_url)
    return r.json()["cookie"]


def send_answer(answer):
    "Send response"
    answer_url = f"https://tasks.aidevs.pl/answer/{token}"
    payload = {"answer": answer}
    return requests.post(url=answer_url, json=payload)


token = authorize(task_name=task_name)
answer = get_input_data(token=token)
response = send_answer(answer=answer)
print(response.json())
