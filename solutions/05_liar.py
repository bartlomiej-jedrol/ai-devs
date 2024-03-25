from lib.handle_task import get_token, get_task, send_answer

# from openai_models import models
# from openai import OpenAI
import logging

# import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get token

task_name = "liar"
token = get_token(task_name=task_name)

# Get task details
get_task(token=token)
