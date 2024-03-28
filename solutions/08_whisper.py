import logging
import requests
import os
from typing import Optional

from urllib.parse import urlparse
from openai import OpenAI

from lib.get_model import get_model
from lib.handle_task import get_task_token, get_task_details, send_answer

logger = logging.getLogger()


def get_substring(s, char) -> str:
    """Return substring for a given string and character."""
    index = s.find(char)
    if index == -1:
        return ""
    else:
        return s[index:]


def validate_url(url) -> bool:
    """Validate if it is a correct url."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError as e:
        logger.error("Validation for the url failed. Error message: %s.", e)
        return False


def get_file_name(file_url) -> str:
    """Get file name for a given url."""
    parsed_url = urlparse(file_url)
    return os.path.basename(parsed_url.path)


def download_file(file_url, file_name, folder_name) -> bool:
    """Download file for a given url. Save the file into a given folder. Return True if downloading the succeeded."""
    try:
        # Get a file from the url
        response = requests.get(url=file_url, stream=True)
        if response.status_code == 200:
            logger.info("Downloading the file succeeded.")

            # Create a directory if does not exist
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            # Save file to the local directory
            try:
                with open(os.path.join(folder_name, file_name), "wb") as f:
                    f.write(response.content)
                return True
            except IOError as e:
                logger.error("Writing the fail failed: %s", e)
                return False
        else:
            logger.error(
                "Downloading the file failed. Status code: %s", response.status_code
            )
            return False
    except ValueError as e:
        logger.error("Downloading the file failed. Error message: %s.", e)
        return False


def create_transcription(file_name, folder_name) -> Optional[str]:
    """Create transcription for a given file. Return the transcription."""
    client = OpenAI()

    # Get model name from model list
    model = get_model("whisper")

    try:
        # Open the audio file
        with open(os.path.join(folder_name, file_name), "rb") as audio_file:
            # Send the request for transcription creation
            transcription = client.audio.transcriptions.create(
                model=model, file=audio_file
            )
            logger.info("Transcription creation succeeded.")
        return transcription.text
    except ValueError as e:
        logger.error(
            "Transcription creation failed. Error message: %s. Response: %s.",
            e,
            transcription,
        )
        return None


def main():
    """Retrieve the .mp3 file from the ai_devs server. Transcribe the .mp3 file using the OpenAI's Whisper model."""
    # Authorize the task and get the task details
    ai_devs_task_token = get_task_token(task_name="whisper")
    response = get_task_details(token=ai_devs_task_token)

    # Extract the file url
    task_message = response["msg"]
    file_url = get_substring(get_substring(s=task_message, char=":"), "h")

    # Check if file url is a correct url
    if validate_url(file_url):
        # Get the file name from the file url
        file_name = get_file_name(file_url=file_url)

        # Save the file to the local folder
        folder_name = "downloads"
        if download_file(
            file_url=file_url, file_name=file_name, folder_name=folder_name
        ):
            # Create transcription for a given file
            transcription = create_transcription(
                file_name=file_name, folder_name=folder_name
            )

            # Send the transcription as an answer to the ai_devs api
            if transcription is not None:
                print(send_answer(token=ai_devs_task_token, answer=transcription))


main()
