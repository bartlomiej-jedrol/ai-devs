import logging
import requests
import os
import re
import json
from typing import Optional, Union, List, Dict, Any

from urllib.parse import urlparse

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


def extract_urls(text: str):
    "Extract urls from a given string."
    url_regex = r"https?://\S+\.json(?=\s|$)"

    urls = re.findall(url_regex, text)

    if len(urls) > 0:
        return urls[0]
    return None


def retrieve_json_data_from_url(json_url: str) -> Optional[List[Dict[str, Any]]]:
    """Retrieve JSON data from URL."""
    try:
        response = requests.get(url=json_url)
        response.raise_for_status()

        json_data = response.json()
        with open("response.json", "w") as f:
            json.dump(json_data, f)

        logger.info("Successfully retrieved JSON data from URL")
        return json_data
    except Exception as e:
        logger.error(f"Failed to retrieve JSON data from URL: {e}")
        return None


def download_file(file_url, file_name, folder_name) -> bool:
    """Download file for a given url. Save the file into a given folder. Return True if downloading the succeeded."""
    if validate_url(url=file_url):
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


def send_request(url: str) -> Union[Dict, List[Dict]]:
    """Send a request to the API."""
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        response_json = response.json()
        logger.info(f"Successfully retrieved data from the API")
        return response_json
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to the API failed: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode the API response: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None
