import logging
from typing import Optional, Dict, List

logger = logging.getLogger()


def create_completion(
    client: str,
    messages: Optional[List[Dict[str, str]]],
    model: str,
    tools: Dict = None,
    response_format: Dict = None,
) -> Optional[str]:
    """Call OpenAI's Chat completion API."""
    if tools is not None:
        try:
            completion = client.chat.completions.create(
                messages=messages, model=model, tools=tools, temperature=0
            )
            response = completion.model_dump()
            logger.info(f"Successfully created completion: {response}")
            return response["choices"][0]["message"]["tool_calls"][0]["function"][
                "arguments"
            ]
        except ValueError as e:
            logger.error(e)
            return None
    elif response_format is not None:
        try:
            completion = client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=0,
                response_format=response_format,
            )
            response = completion.model_dump()
            logger.info(f"Successfully created completion: {response}")
            return response["choices"][0]["message"]["content"]
        except ValueError as e:
            logger.error(e)
            return None
    else:
        try:
            completion = client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=0,
            )
            response = completion.model_dump()
            logger.info(f"Successfully created completion: {response}")
            return response["choices"][0]["message"]["content"]
        except ValueError as e:
            logger.error(e)
            return None
