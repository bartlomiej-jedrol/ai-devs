from lib.handle_task import get_token, get_task_details, send_answer
from openai import OpenAI
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get token
task_name = "moderation"
token = get_token(task_name=task_name)

# Get task details
task = get_task_details(token=token)
messages = task["input"]

# Call the OpenAI moderation API to verify if the statement goes through moderation.
client = OpenAI()
model = "text-moderation-latest"
moderation_results = []
for message in messages:
    try:
        response = client.moderations.create(model=model, input=message).model_dump()

        logger.info(f"Successfully called the Moderation API: {response}.\n")
    except Exception as e:
        print(e)
        print("Error at the time of calling the Moderation API.\n")

    flagged = response["results"][0]["flagged"]
    if flagged:
        moderation_results.append(1)
    elif not flagged:
        moderation_results.append(0)

# The task is to POST the moderation results
answer = moderation_results
send_answer(token=token, answer=answer)
