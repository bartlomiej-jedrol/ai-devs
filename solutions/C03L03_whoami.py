import logging
import json
from typing import Optional

from openai import OpenAI

from lib.handle_task import get_task_token, get_task_details, send_answer
from lib.get_model import get_model

logger = logging.getLogger()


def create_completion(client, messages, model) -> Optional[str]:
    """Call the Chat completion api."""
    try:
        # Send a request to the Chat completion api.
        completion = client.chat.completions.create(
            messages=messages, model=model, temperature=0
        )
        # Generate a dictionary of the completion
        response = completion.model_dump()
        return response["choices"][0]["message"]["content"]
    except ValueError as e:
        logger.error(e)
        return None


def capitalize_sentences(client: str, model: str, text: str) -> Optional[str]:
    """Capitalize sentences in the text using the Chat completion api."""
    # Prepare message for the api request
    messages = []
    messages.append(
        {"role": "system", "content": "Capitalize first letter of each sentence."}
    )
    messages.append({"role": "system", "content": text})

    # Send a request to the Chat completion api.
    return create_completion(client=client, model=model, messages=messages)


def main():
    """With use of the OpenAI API guess who is the famous person based of provided hints from the ai_devs server."""
    # Set initial values
    is_not_guessed = True
    hint_list = []
    client = OpenAI()
    model = get_model("gpt4")

    # Get hints until the OpenAI model is not sure about the famous person.
    while is_not_guessed:
        # Get task details from the ai_devs server.
        ai_devs_task_token = get_task_token("whoami")

        # Build context for the OpenAI model.
        hint = get_task_details(token=ai_devs_task_token)["hint"]
        hint_list.append(hint)
        context = f"{'. '.join(hint_list)}."

        # Capitalize context with use of the OpenAI model.
        capitalized_context = capitalize_sentences(
            client=client, model=model, text=context
        )

        # Prepare parameters for the OpenAI API request (for guessing the famous person).
        messages = []
        messages.append(
            {
                "role": "system",
                "content": f"""
                Use the context to guess the famous person. Represent the response as a JSON object using this format:

                JSON:```
                {{
                    "guessed": "YES|NO",
                    "famousPerson": "guessed person|''"
                }}
                ```

                Rules:```
                - "guessed" - if you guessed the famous person return YES, otherwise return NO. Return YES only if you are fully sure about the person. If you are unsure return NO.
                - "famousPerson": if you guessed return the name and surname of the famous person. Otherwise return an empty string ''.
                - Respond in the JSON format and nothing else. Do not wrap JSON with back-ticks or quotes.
                ```

                Examples:```
                - context: "In 1990, his popularity increased dramatically when he starred in the popular television series The Fresh Prince of Bel-Air. He has received Best Actor Oscar nominations for Ali and The Pursuit of Happyness."
                - response:
                {{
                    "guessed": "YES",
                    "famousPerson": "Will Smith"
                }}
                ```

                Context: {capitalized_context}
                """,
            }
        )

        # Get response from the OpenAI API on the famous person.
        completion = create_completion(client=client, model=model, messages=messages)

        # Parse response from the OpenAI API.
        completion_data = json.loads(completion)
        guessed = completion_data["guessed"]
        famous_person = completion_data["famousPerson"]

        # Check if the OpenAI model guessed who is the famous person.
        if guessed == "YES":
            is_not_guessed = False

    # Send the guessed person to the ai_devs server.
    send_answer(token=ai_devs_task_token, answer=famous_person)


main()
