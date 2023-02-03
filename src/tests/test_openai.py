import requests
from typing import Any
from utils.configparser import parse_config
import json


class Openai:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self.config = parse_config()

    def make_request(self, prompt: str) -> Any:
        if self.api_key is None:
            self.api_key = self.config["gtp3"]["apikey"]
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        url = "https://api.openai.com/v1/completions"
        payload = json.dumps({
            "model": "text-davinci-002",
            "prompt": f"{prompt}",
            "temperature": 0,
            "max_tokens": int(self.config["gtp3"]["maxtoken"]) - len(prompt)
        })
        r = requests.post(url, headers=headers, data=payload)
        return r.json()

    def validate(self) -> Any:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.config["gtp3"]["apikey"]}'
        }
        url = "https://api.openai.com/v1/completions"
        payload = json.dumps({
            "model": "text-davinci-002",
            "prompt": "Say this is a test",
            "temperature": 0,
            "max_tokens": 1
        })
        r = requests.post(url, headers=headers, data=payload)
        return r.json()

    def __str__(self) -> Any:
        return self.api_key


def test_openai() -> None:
    openai = Openai()
    validation = openai.validate()
    if validation.get('error', None) is not None:
        raise Exception(f'OpenAI request was not successful: {validation["error"]["message"]}')


def test_make_request() -> None:
    openai = Openai()
    assert openai.make_request("Whats 2 multiplied 2") is not None
