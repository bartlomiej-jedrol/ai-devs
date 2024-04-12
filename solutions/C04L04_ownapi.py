from lib.handle_task import get_task_token, send_answer


def main():
    """Send answer for ai_devs task."""
    ai_devs_task_token = get_task_token(task_name="ownapi")

    send_answer(
        token=ai_devs_task_token,
        answer="https://be85-83-10-26-164.ngrok-free.app/question",
    )


main()
