import logging
import requests
import re
import uuid
from typing import Optional, Tuple, List, Dict, Any

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException
from qdrant_client.models import VectorParams, Distance, Batch

from lib.handle_task import get_task_token, get_task_details, send_answer
from lib.get_model import get_model

logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)
logger = logging.getLogger()

COLLECTION_NAME = "unknown_urls_info"
MODEL = get_model("embedding")


def initialize_qdrant_client(host: str, port: int) -> Optional[QdrantClient]:
    """Initialize Qdrant client."""
    try:
        qdrant_client = QdrantClient(host=host, port=port)

        # Check if the test collection can be created
        if not recreate_qdrant_collection(
            qdrant_client=qdrant_client, collection_name="test_connection"
        ):
            return None

        logger.info("Successfully initialized and tested Qdrant client")
        return qdrant_client
    except ResponseHandlingException as e:
        logger.error(f"Failed to initialize Qdrant client: {e}")
        return None


def recreate_qdrant_collection(
    qdrant_client: QdrantClient, collection_name: str
) -> Optional[str]:
    """Recreate Qdrant collection."""
    try:
        vectors_config = VectorParams(size=1536, distance=Distance.COSINE)
        qdrant_collection = qdrant_client.recreate_collection(
            collection_name=collection_name, vectors_config=vectors_config
        )
        logger.info("Successfully (re)created Qdrant collection")
        return qdrant_collection
    except Exception as e:
        logger.error(f"Failed to (re)create Qdrant collection - {collection_name}: {e}")
        return None


def retrieve_input_from_task(task_name: str) -> Tuple[str, str, str]:
    """Retrieve question and JSON url from ai_devs server."""
    ai_devs_task_name = task_name
    ai_devs_task_token = get_task_token(task_name=ai_devs_task_name)
    task_details_response = get_task_details(token=ai_devs_task_token)
    question = task_details_response["question"]
    json_url = _extract_urls(text=task_details_response["msg"])
    return question, json_url, ai_devs_task_token


def _extract_urls(text: str):
    "Extract urls from a given string."
    url_regex = r"https?://\S+\.json(?=\s|$)"

    urls = re.findall(url_regex, text)

    if len(urls) > 0:
        return urls[0]
    return None


def retrieve_json_data_from_url(json_url: str) -> Optional[List[Dict[str, Any]]]:
    """Retrieve JSON data from the unknown server."""
    try:
        response = requests.get(url=json_url)
        response.raise_for_status()
        logger.info(f"Successfully retrieved JSON data from URL")
        return response.json()
    except Exception as e:
        logger.error(f"Failed to retrieve JSON data from URL: {e}")
        return None


def upsert_qdrant_points(
    openai_client: OpenAI,
    qdrant_client: QdrantClient,
    collection_name: str,
    json_data: List[Dict[str, str]],
):
    """Upsert Qdrant points for given JSON data."""
    ids = []
    payloads = []
    vectors = []

    # Prepare points
    for json_item in json_data:
        ids.append(str(uuid.uuid4()))
        payloads.append(json_item)
        vectors.append(
            create_embedding(client=openai_client, model=MODEL, input=json_item["info"])
        )

    try:
        qdrant_client.upsert(
            collection_name=collection_name,
            points=Batch(
                ids=ids,
                payloads=payloads,
                vectors=vectors,
            ),
        )
        logger.info("Successfully upserted points to Qdrant")
    except Exception as e:
        logger.error(f"Failed to upsert points to Qdrant: {e}")


def create_embedding(client: str, model: str, input: str) -> Optional[str]:
    """Create embedding for a given string using the OpenAI's embeddings API."""
    try:
        response = client.embeddings.create(model=model, input=input)
        embedding = response.model_dump()
        logger.info(f"Successfully obtained response from the embeddings API")
        return embedding["data"][0]["embedding"]
    except Exception as e:
        logger.error(f"Failed to request embeddings from the embeddings API: {e}")
        return None


def search_for_point(
    qdrant_client: QdrantClient,
    openai_client: OpenAI,
    collection_name: str,
    question: str,
) -> Optional[str]:
    """Search for Qdrant point similar to question."""
    question_vector = create_embedding(
        client=openai_client, model=MODEL, input=question
    )

    try:
        answer = qdrant_client.search(
            collection_name=collection_name,
            query_vector=question_vector,
            limit=1,
        )
        logger.info("Successfully searched for point in Qdrant")
        return answer[0].payload["url"]
    except Exception as e:
        logger.error(f"Failed to search for point in Qdrant: {e}")
        return None


def count_points(
    qdrant_client: QdrantClient, collection_name: str  # , ids: List[int]
) -> Optional[int]:
    """Return number of Qdrant collection's points."""
    try:
        response = qdrant_client.get_collection(collection_name=collection_name)
        logger.info("Successfully retrieved Qdrant collection's points")
        return response.points_count
    except Exception as e:
        logger.error(f"Failed to retrieve Qdrant collection's points: {e}")
        return None


def get_answer():
    """
    Get answer from Qdrant collection for question from ai_devs.
    The Qdrant collection contains points based on JSON data from the unknown server.
    """
    qdrant_client = initialize_qdrant_client(host="localhost", port=6333)
    if not qdrant_client:
        return None

    question, json_url, ai_devs_task_token = retrieve_input_from_task(
        task_name="search"
    )

    json_data = retrieve_json_data_from_url(json_url=json_url)

    points_count = count_points(
        qdrant_client=qdrant_client,
        collection_name=COLLECTION_NAME,
    )
    if points_count != 128:
        # Create collection if points do not exist. Number of points is hardcoded to 128.
        qdrant_collection = recreate_qdrant_collection(
            qdrant_client=qdrant_client, collection_name=COLLECTION_NAME
        )
        if not qdrant_collection:
            return None

        # Upsert points to the collection
        upsert_qdrant_points(
            openai_client=openai_client,
            qdrant_client=qdrant_client,
            collection_name=COLLECTION_NAME,
            json_data=json_data,
        )

    openai_client = OpenAI()

    answer = search_for_point(
        qdrant_client=qdrant_client,
        openai_client=openai_client,
        collection_name=COLLECTION_NAME,
        question=question,
    )

    send_answer(token=ai_devs_task_token, answer=answer)


get_answer()
