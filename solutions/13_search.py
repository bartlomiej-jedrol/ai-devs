import logging
import requests
import re
from typing import Optional, Tuple, List, Dict, Any

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException
from qdrant_client.models import VectorParams, Distance

from lib.handle_task import get_task_token, get_task_details

logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger()


def initialize_qdrant_client(host: str, port: int) -> Optional[QdrantClient]:
    """Initialize qdrant client."""
    try:
        qdrant_client = QdrantClient(host=host, port=port)

        test_collection = "test_connection"
        vectors_config = VectorParams(size=1536, distance=Distance.COSINE)
        qdrant_client.recreate_collection(
            collection_name=test_collection, vectors_config=vectors_config
        )
        if qdrant_client.collection_exists(test_collection):
            logger.info("Successfully tested Qdrant connection.")
            # qdrant_client.delete_collection(collection_name=test_collection)

        return qdrant_client
    except ResponseHandlingException as e:
        logger.error(f"Failed to initialize Qdrant client: {e}")
        return None


def retrieve_input_from_task(task_name: str) -> Tuple[str, str]:
    """Retrieve question and JSON url from ai_devs server."""
    ai_devs_task_name = task_name
    ai_devs_task_token = get_task_token(task_name=ai_devs_task_name)
    task_details_response = get_task_details(token=ai_devs_task_token)
    question = task_details_response["question"]
    json_url = _extract_urls(text=task_details_response["msg"])
    return question, json_url


def _extract_urls(text: str):
    "Extract urls from a given string."
    url_regex = r"https?://\S+\.json(?=\s|$)"

    urls = re.findall(url_regex, text)

    if len(urls) > 0:
        return urls[0]
    return None


def retrieve_json_data_from_url(json_url: str) -> Optional[List[Dict[str, Any]]]:
    try:
        response = requests.get(url=json_url)
        response.raise_for_status()
        logger.info(f"Successfully retrieved JSON data from URL")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to retrieve JSON data from URL: {e}")
        return None


def get_answer():
    """
    Get answer from Qdrant collection for question from ai_devs.
    The Qdrant collection contains points based on JSON data from the unknown server.
    """
    question, json_url = retrieve_input_from_task(task_name="search")

    json_data = retrieve_json_data_from_url(json_url=json_url)

    qdrant_client = initialize_qdrant_client(host="localhost", port=6333)
    print(qdrant_client)


get_answer()
