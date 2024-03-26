from openai import OpenAI
import json

MODEL = "gpt-4-0125-preview"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Knock knock."},
]

client = OpenAI()
response = client.chat.completions.create(messages=messages, model=MODEL, temperature=0)
print(type(response))

response_dict = response.model_dump()
response_json = json.dumps(response_dict, indent=4)

print(response_json)
