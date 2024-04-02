import requests
import logging

from requests.adapters import HTTPAdapter, Retry
from openai import OpenAI

from lib.handle_task import get_task_token, get_task_details, send_answer
from lib.get_model import get_model

logger = logging.getLogger()


def create_completion(client, messages, model):
    """Call the Chat completion api."""
    try:
        completion = client.chat.completions.create(
            messages=messages, model=model, temperature=0
        )

        response = completion.model_dump()
        return response["choices"][0]["message"]["content"]
    except ValueError as e:
        logger.error(e)
        return None


def get_article(article_url) -> str:
    """Get an article from the ai_devs server."""
    try:
        # Set retry mechanism
        s = requests.Session()
        retry_mechanism = Retry(total=3, backoff_factor=1, status_forcelist=[500])
        s.mount("https://", HTTPAdapter(max_retries=retry_mechanism))

        # Set headers for the request. User-Agent is set to act as a browser in order not to be blocked by the server as bot.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        # Send request to the ai_devs server
        response = s.get(url=article_url, headers=headers)
        return response.text
    except ValueError as e:
        logger.error(
            f"Error occurred at the time of accessing article: {response.status_code}"
        )


def main():
    # Get task details from ai_devs API
    ai_devs_task_token = get_task_token("scraper")
    response = get_task_details(token=ai_devs_task_token)
    question_for_article = response["question"]
    article_url = response["input"]

    # Get article from the ai_devs server
    article = get_article(article_url=article_url)

    # Prepare parameters for the Chat completion API request
    messages = []
    messages.append(
        {
            "role": "system",
            "content": f"""
            As an assistant you answer question to the article provided in the  context.
            
            context```
            {article}
            ```
            """,
        }
    )
    messages.append({"role": "user", "content": f"{question_for_article}"})
    client = OpenAI()
    model = get_model("gpt4")

    # Send request to the Chat completion API
    answer = create_completion(client=client, model=model, messages=messages)

    # Send an answer to the ai_devs server
    send_answer(token=ai_devs_task_token, answer=answer)


main()
