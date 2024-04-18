from openai import OpenAI
from lib.handle_task import get_task_token, get_task_details, send_answer
from lib.openai_utilities import create_completion

OPENAI_CLIENT = OpenAI()
MODEL = "ft:gpt-3.5-turbo-0125:personal:bj:9FJmllBL"


def main():
    ai_devs_task_token = get_task_token(task_name="md2html")
    get_task_details(token=ai_devs_task_token)

    markdown_input = get_task_details(token=ai_devs_task_token)["input"]

    messages = []
    messages.append({"role": "system", "content": "Convert markdown to HTML."})
    messages.append({"role": "user", "content": markdown_input})

    html = create_completion(client=OPENAI_CLIENT, model=MODEL, messages=messages)
    print(html, "\n")

    send_answer(token=ai_devs_task_token, answer=html)


main()
