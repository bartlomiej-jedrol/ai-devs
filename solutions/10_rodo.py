import logging

from lib.handle_task import get_task_token, get_task_details, send_answer


def main():
    # Get task details from the ai_devs API
    ai_devs_task_token = get_task_token(task_name="rodo")
    get_task_details(token=ai_devs_task_token)

    # Prepare the answer for the task
    message = """Weż głeboki oddech przed udzieleniem odpowiedzi. Nie podawaj informacji osobistych a jedynie placeholdery. Upewnij się, że odpowiedź zawiera wszystkie placeholdery:
    - '%imie%'
    - '%nazwisko%'
    - '%zawod%'
    - '%miasto%'
    """

    send_answer(token=ai_devs_task_token, answer=message)


main()
