import requests
from tests.test_wordpress_jwt import Wpjwt
from dataclasses import dataclass, field, asdict
from utils.configparser import parse_config
from datetime import datetime
from typing import Any, Dict, TypeVar, Generic
import json


T = TypeVar('T')
Json = dict[str, 'Json'] | list['Json'] | str | int | float | bool | None


@dataclass
class Blogpost(Generic[T]):
    title: str
    content: Dict[str, Any] = field(default_factory=lambda: dict())
    # list of id's of the corresponding categories
    # categories: list[int] = field(default_factory=lambda: [2])
    categories: list[int] = field(default_factory=lambda: [3])
    # list of id's of the corresponding tags
    # tags: list[int] = field(default_factory=lambda: [3])
    tags: list[int] = field(default_factory=lambda: [4])
    sticky: bool = field(default=False)
    date: str | None = field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status: str = field(default='publish')
    meta: Dict[str, Any] = field(default_factory=lambda: dict())
    featured_media: int | None = field(default=None)

    def to_json(self) -> Json:
        return json.dumps(asdict(self))


class WordpressController:
    def __init__(self, token: str | None = None):
        wp_connection = Wpjwt(token=token)
        self.token = token if token is not None else wp_connection.get_token()['token']
        self.config = parse_config()

    @property
    def jwt_token(self) -> Any:
        return self.token

    def get_all_posts(self) -> Any:
        headers = {"Authorization": f"Bearer {self.token}"}
        r = requests.get(f'{self.config["wordpress"]["host"]}/wp-json/wp/v2/posts', headers=headers)
        return r.json()

    def create_post(self, blogpost: Blogpost[T]) -> Any:
        headers = {"Authorization": f"Bearer {self.token}",
                   "Content-type": "application/json"}
        r = requests.post(f'{self.config["wordpress"]["host"]}/wp-json/wp/v2/posts', headers=headers,
                          data=blogpost.to_json())
        if r.status_code != 201:
            raise Exception(f'Error creating post: \n {r.json()}')
        return r.json()

    def upload_media(self, image_path: str, title: str, caption: str, alt_text: str) -> Any:
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "title": title,
            "caption": caption,
            "alt_text": alt_text
        }
        r = requests.post(f'{self.config["wordpress"]["host"]}/wp-json/wp/v2/media', headers=headers,
                          files={'file': open(image_path, 'rb')}, data=data)
        return r.json()['id']
