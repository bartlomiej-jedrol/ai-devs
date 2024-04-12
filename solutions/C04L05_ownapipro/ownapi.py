import os
import signal
import json
from typing import Optional, Dict, Tuple

from openai import OpenAI
from flask import Flask, jsonify, request

from lib.get_model import get_model
from lib.openai_utilities import create_completion

OPENAI_CLIENT = OpenAI()
MODEL = get_model("gpt4")
context = None


def handle_get_request():
    """Handle GET request."""
    return {"test": "test"}, 200


def classify_user_message(question: str) -> Dict[str, str]:
    """Classify user message (question from ai_devs) to one of the following types:
    - question
    - information
    """
    # Set context to an empty string if there is no context to be provided (for questions)
    global context
    if not context:
        context = ""

    # Prepare messages
    messages = []
    messages.append(
        {
            "role": "system",
            "content": f"""Classify a user message.
            Respond with a JSON object: message (original user message), message_type (question|information), answer (respond to question|confirm information).
            rules:
            - answer must be concise
            - answer must be in Polish
            context: {context}
            """,
        }
    )
    messages.append({"role": "user", "content": question})

    # Call OpenAI
    response = create_completion(
        client=OPENAI_CLIENT,
        model=MODEL,
        messages=messages,
        response_format={"type": "json_object"},
    )
    response_data = json.loads(response)
    print(f"Response data: {response_data}")

    return response_data


def prepare_answer(response_data: Tuple[str, str]):
    """Prepare response based on message type from OpenAI."""
    message_type = response_data.get("message_type")
    answer = response_data.get("answer")

    # No context is needed in case of question.
    # For information - the context is needed to be used once the question is asked.
    if message_type == "question":
        context = None
    elif message_type == "information":
        context = response_data.get("message")
    print(f"Context: {context}")
    print(f"Answer: {answer}")

    return context, answer


def main():
    """Run API.
    - localhost: http://localhost:5000
    - ngrok: https://be85-83-10-26-164.ngrok-free.app/question
    """
    # Initialize Flask app
    app = Flask("api")

    # Describe endpoints
    @app.route("/api", methods=["GET"])
    def get_data():
        data = handle_get_request()
        return jsonify(data)

    @app.route("/question", methods=["POST"])
    def post_data():
        print(f"Request JSON data: {request.json}")
        question = request.json.get("question")
        print(f"User question is: {question}\n")

        # Generate response data
        response_data = classify_user_message(question=question)

        # Prepare answer for ai_devs
        # Set context for an actual question that may come in a next request
        global context
        context, answer = prepare_answer(response_data=response_data)

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
