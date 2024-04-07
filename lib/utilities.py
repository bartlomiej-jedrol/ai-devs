import logging
import requests
import os

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
