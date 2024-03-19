from handle_task import get_token, get_task, send_answer

task_name = "helloapi"
token = get_token(task_name=task_name)
task = get_task(token=token)
# The task is to to POST value of "cookie"
answer = task["cookie"]
send_answer(token=token, answer=answer)
