from tempfile import NamedTemporaryFile
import requests
from typing import Any


class Tempfile:

    def __init__(self, url: str):
        self.url = url
        self.file = self.create_temporary_file(self.url)

    def create_temporary_file(self, url: str) -> Any:
        raw = requests.get(url).content
        with NamedTemporaryFile(delete=False, mode="wb", suffix=".jpg") as img:
            img.write(raw)
            return img

    def delete(self) -> None:
        self.file.close()
