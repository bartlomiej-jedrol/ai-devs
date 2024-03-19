import os
import requests
from openai import OpenAI


API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
model = "text-embedding-ada-002"


def call_embeddings():
    """Call embeddings endpoint using requests library."""
    payload = {"input": "Bartek", "model": model}
    r = requests.post(url=EMBEDDINGS_URL, headers=headers, json=payload)
    print(r.json())


def get_embeddings():
    """Get embeddings."""
    client = OpenAI()
    response = client.embeddings.create(input="Bartek", model=model)
    print(response)


def get_completion():
    """Get completion."""
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "system",
                "content": "Capital river",
            },
            {"role": "user", "content": "Rzeczpospolita Polska"},
        ],
    )
    print(response)


# get_embeddings()
get_completion()
