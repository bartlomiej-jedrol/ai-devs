from handle_task import authorize, get_input_data, send_answer

task_name = "helloapi"

token = authorize(task_name=task_name)
answer = get_input_data(token=token)
response = send_answer(answer=answer)
print(response.json())
