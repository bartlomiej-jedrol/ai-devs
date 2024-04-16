from lib.handle_task import get_task_token, get_task_details, send_answer

task_name = "helloapi"
token = get_task_token(task_name=task_name)
task = get_task_details(token=token)
# The task is to to POST value of "cookie"
answer = task["cookie"]
send_answer(token=token, answer=answer)
