import requests
from typing import Dict, Any
from utils.configparser import parse_config
from utils.cache_token import timed_lru_cache


class Wpjwt:
    def __init__(self, token: str | None = None):
        self.token = token
        self.config = parse_config()

    @timed_lru_cache(604800)  # type: ignore
    def get_token(self) -> Any | Dict[str, Any]:
        if self.token is None:
            payload = {'username': self.config['wordpress']['username'],
                       'password': self.config['wordpress']['password']}
            r = requests.post(f'{self.config["wordpress"]["host"]}/wp-json/jwt-auth/v1/token', data=payload)
            if r.json()["success"] is False:
                return r.json()
            return {"token": r.json()['data']['token'], "success": True}
        else:
            return self.token

    def validate(self, token: str) -> Any:
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.post(f'{self.config["wordpress"]["host"]}/wp-json/jwt-auth/v1/token/validate', headers=headers)
        return r.json()['success']

    def __str__(self) -> Any:
        return self.token


def test_wordpress_jwt() -> None:
    wordpress = Wpjwt()
    token = wordpress.get_token()
    if token['success'] is False:
        raise Exception('JWT Token request was not successful')
    validation = wordpress.validate(token=token['token'])
    assert validation is True
