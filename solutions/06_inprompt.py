import logging

from lib.get_model import get_model
from openai import OpenAI

from lib.handle_task import (
    get_token,
    get_task_details,
    send_answer,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_completion(client, messages, model):
    """Call the Chat completion api"""
    try:
        completion = client.chat.completions.create(
            messages=messages, model=model, temperature=0
        )

        response = completion.model_dump()
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        logger.error(e)
        return None


def main():
    """Answer a given question using the context provided by the ai_devs api"""
    model = get_model("gpt4")
    client = OpenAI()

    # Get task details
    token = get_token(task_name="inprompt")
    task = get_task_details(token=token)

    question = task["question"]

    # Indicate what's the name of the person from the question
    messages = [
        {
            "role": "system",
            "content": """Return a name of the person from a given string. Return only a name of the person, nothing else. 
        Examples```

        - string: Konrad ma niebieskie oczy, długie włosy i pracuje jako fryzjer, a na śniadanie najbardziej lubi jeść kanapki z serem
        - response: Konrad

        - string: Kajfasz ma czarne oczy, krótkie włosy i pracuje jako kucharz, a na śniadanie najbardziej lubi jeść parówki
        - response: Kajfasz
        ```
        """,
        },
        {"role": "user", "content": f"{question}"},
    ]
    name = create_completion(client=client, messages=messages, model=model)

    if name != None:
        # Filter out records to those related to the person from the question
        records_list = task["input"]
        filtered_record_list = []
        for record in records_list:
            if name in record:
                filtered_record_list.append(record)

        # Answer a given question using the filtered out records related to the person
        messages = [
            {
                "role": "system",
                "content": f"""Answer a given question using the context provided below and nothing else.
                    
                Example```
                - question: Co najbardziej lubi jeść Konstanty?
                - context: Konstanty ma brązowe oczy, długie włosy i pracuje jako dziennikarz, a na śniadanie najbardziej lubi jeść bułkę z bananem
                - answer: bułkę z bananem
                ```

                Context```
                {filtered_record_list}
                ```
            """,
            },
            {"role": "user", "content": f"{question}"},
        ]
        answer = create_completion(client=client, messages=messages, model=model)

        if answer != None:
            # Send an answer to the question to the ai_devs api
            send_answer(token=token, answer=answer)


main()
