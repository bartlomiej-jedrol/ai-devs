import requests
import os

from lib.handle_task import get_task_token, get_task_details, send_answer


def main():
    """Send answer for ai_devs task."""
    ai_devs_task_token = get_task_token(task_name="meme")

    # RenderForm API
    render_from_api_key = os.getenv("RENDER_FORM_API_KEY")
    render_form_url = "https://get.renderform.io/api/v2/render"
    render_form_template_id = "quick-ghouls-feed-gently-1889"

    # Get task details
    task_details = get_task_details(token=ai_devs_task_token)
    mem_text = task_details["text"]
    mem_image_url = task_details["image"]

    # Set data for RenderForm template
    headers = {"X-API-KEY": render_from_api_key, "Content-Type": "application/json"}
    data = {
        "template": render_form_template_id,
        "data": {
            "my-text.text": mem_text,
            "my-image.src": mem_image_url,
        },
    }

    # Send request to RenderForm API
    try:
        response = requests.post(url=render_form_url, headers=headers, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to request the RenderForm API: {e}")

    # Send answer to ai_devs
    send_answer(token=ai_devs_task_token, answer=response.json()["href"])


main()
