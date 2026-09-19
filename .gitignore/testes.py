import json
import os

import requests

response = requests.post(
    "https://api.meta.ai/v1/responses/input_tokens",
    headers={
        "Authorization": f"Bearer {os.environ['MODEL_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "muse-spark-1.3-contributor",
        "input": "What is the capital of France?",
    },
)
response.raise_for_status()
print(response.json()["input_tokens"])