import json

MODEL_LIST = "openai_models/model_list.json"

with open(MODEL_LIST, "r", encoding="utf-8") as f:
    data = json.load(f)


def get_model(short_name):
    """Return model for the provided short name."""
    for model in data["models"]:
        if model.get("short_name") and model.get("short_name") == short_name:
            return model["name"]
