import logging
from typing import Optional

logger = logging.getLogger()


def create_completion(client, messages, model) -> Optional[str]:
    """Call OpenAI's Chat completion API."""
    try:
        completion = client.chat.completions.create(
            messages=messages, model=model, temperature=0
        )
        response = completion.model_dump()
        return response["choices"][0]["message"]["content"]
    except ValueError as e:
        logger.error(e)
        return None
