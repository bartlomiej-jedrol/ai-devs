import logging
import json

from openai import OpenAI

from lib.get_model import get_model
from lib.handle_task import get_task_token, send_answer

logger = logging.getLogger()


def get_function_specification():
    """Get the function specification for the addUser function."""
    return [
        {
            "type": "function",
            "function": {
                "name": "addUser",
                "description": "add user based on properties",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "provide name of the user",
                        },
                        "surname": {
                            "type": "string",
                            "description": "provide surname of the user",
                        },
                        "year": {
                            "type": "integer",
                            "description": "provide year of birth of the user",
                        },
                    },
                },
            },
        }
    ]


def create_completion(client: str, model: str, messages: list, tools: dict):
    """Create a completion using the OpenAI's Completions API."""
    # Send messages to the Completions API
    try:
        completion = client.chat.completions.create(
            model=model, messages=messages, tools=tools
        )
        logger.info(f"Successfully created completion: {completion}")
        return completion
    except Exception as e:
        logger.error(f"Error occurred while creating completion: {e}")
        raise


def main():
    """Create function with name addUser."""
    # Set parameters for the Completions API call
    client = OpenAI()
    MODEL = get_model("gpt4")
    messages = []
    messages.append(
        {"role": "system", "content": "Add user based on provided properties."}
    )
    messages.append(
        {"role": "user", "content": "Hello, my name is John Doe. I was born in 1990."}
    )
    tools = get_function_specification()

    # Create a completion using the OpenAI's Completions API
    completion = create_completion(
        client=client, model=MODEL, messages=messages, tools=tools
    )

    # Extract the user data from the response
    response_data = completion.model_dump()
    arguments = (
        response_data.get("choices", [{}])[0]
        .get("message", {})
        .get("tool_calls", [{}])[0]
        .get("function", {})
        .get("arguments")
    )

    # Check if arguments are found
    if arguments is None:
        logger.error("No arguments found.")
        return

    # Extract the user data from the arguments
    arguments_dict = json.loads(arguments)
    user_name = arguments_dict.get("name", "")
    user_surname = arguments_dict.get("surname", "")
    user_year = arguments_dict.get("year", "")

    # Print the user data
    print(f"User {user_name} {user_surname} was born in {user_year}.")

    # Send the answer to the ai_devs API
    ai_devs_task_token = get_task_token(task_name="functions")
    answer = tools[0].get("function", None)

    # Check if answer is found
    if answer is not None:
        send_answer(token=ai_devs_task_token, answer=answer)


main()
