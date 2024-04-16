import logging

from lib.get_model import get_model
from openai import OpenAI

from lib.handle_task import get_task_token, send_answer

logger = logging.getLogger()


def create_embedding(client: str, model: str, input: str):
    """Create embeddings for a given phrase through the OpenAI's embeddings API."""
    try:
        response = client.embeddings.create(model=model, input=input)

        # Dump the API response to dict
        embedding = response.model_dump()

        logger.info(
            f"Successfully obtained response from the embeddings API: {response}"
        )

        # Return the embeddings list
        return embedding["data"][0]["embedding"]

    except Exception as e:
        logger.error(e)
        return None


def main():
    """Create embeddings for a given input. Send it as an answer to the ai_devs API."""
    token = get_task_token(task_name="embedding")
    model = get_model("embedding")
    phrase = "Hawaiian pizza"
    client = OpenAI()

    # Get the embeddings list for a given input
    embedding_list = create_embedding(client=client, model=model, input=phrase)

    send_answer(token=token, answer=embedding_list)


main()
