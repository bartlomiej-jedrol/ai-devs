import os
import signal
import json
from typing import Dict, Tuple

from openai import OpenAI
from flask import Flask, jsonify, request
from serpapi import GoogleSearch

from lib.get_model import get_model
from lib.openai_utilities import create_completion

OPENAI_CLIENT = OpenAI()
MODEL = get_model("gpt4")
SERP_API_KEY = os.getenv("SERP_API_KEY")
SERP_API_GOOGLE_SEARCH_ENDPOINT = "https://serpapi.com/search"


def handle_get_request():
    """Handle GET request."""
    return {"test": "test"}, 200


def extract_search_inputs(question: str) -> Tuple[str, str]:
    """Extract website url and requested resource from the user question."""
    messages = []
    messages.append(
        {
            "role": "system",
            "content": f"""Extract website url and requested resource from that url.
            Respond with a JSON object: website_url, resource
            rules
            - if there is not website url included: website_url: brak
            examples```
            U: Portal onet.pl opublikował kiedyś artykuł odnośnie ataku Rosji na Ukrainę
            S: website_url: onet.pl, resource: artykuł odnośnie ataku Rosji na Ukrainę
            ```
            """,
        }
    )
    messages.append({"role": "user", "content": question})

    response = create_completion(
        client=OPENAI_CLIENT,
        model=MODEL,
        messages=messages,
        response_format={"type": "json_object"},
    )
    response_data = json.loads(response)
    print(f"\tChat completion response data: {response_data}\n")

    return response_data["website_url"], response_data["resource"]


def search_with_serp_api(website_url: str, resource: str) -> str:
    """Search for the resource using the SerpApi Google Search endpoint."""
    # If there is no website url provided, search for the resource directly
    if website_url == "brak":
        search_query = resource
    else:
        search_query = f"site:{website_url} {resource}"

    params = {
        "engine": "google",
        "q": search_query,
    }
    GoogleSearch.SERP_API_KEY = SERP_API_KEY

    search = GoogleSearch(params)
    results = search.get_dict()

    # Get the first organic result
    first_organic_result = results["organic_results"][0]["link"]
    print(f"\tFirst organic result: {first_organic_result}\n")

    return first_organic_result


def answer_ai_devs_question(question: str) -> Dict[str, str]:
    """Answer the ai_devs question."""
    website_url, resource = extract_search_inputs(question=question)

    first_organic_result = search_with_serp_api(
        website_url=website_url, resource=resource
    )

    return first_organic_result


def main():
    """Run API.
    - localhost: http://localhost:5000
    - ngrok: https://d062-37-47-189-49.ngrok-free.app
    """
    # Initialize Flask app
    app = Flask("api")
    app.debug = True

    # Describe endpoints
    @app.route("/api", methods=["GET"])
    def get_data():
        data = handle_get_request()
        return jsonify(data)

    @app.route("/question", methods=["POST"])
    def post_data():
        question = request.json.get("question")
        print(f"\n\tUser question is: {question}\n")

        # Set first organic result as an answer
        answer = answer_ai_devs_question(question=question)

        # Format reply
        formatted_reply = {"reply": answer}
        return formatted_reply

    @app.route("/shutdown", methods=["POST"])
    def shutdown():
        os.kill(os.getpid(), signal.SIGINT)
        return "Server shutting down..."

    # Start app
    app.run()


main()
