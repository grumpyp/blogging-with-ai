import pytest
import configparser
from pathlib import Path


@pytest.fixture
def config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    file = Path(__file__).resolve().parents[2]
    config.read(f'{file}/config.ini')
    return config


class MissingConfigValue(Exception):
    def __init__(self, value_name: str):
        self.value_name = value_name

    def __str__(self) -> str:
        return f'Missing {self.value_name} in config'


def test_gtp3_config(config: configparser.ConfigParser) -> None:
    gtp3_section = config['gtp3']
    if 'apikey' not in gtp3_section:
        raise MissingConfigValue('apikey')


def test_wordpress_config(config: configparser.ConfigParser) -> None:
    wordpress_section = config['wordpress']
    if 'host' not in wordpress_section:
        raise MissingConfigValue('secret')
    if 'username' not in wordpress_section:
        raise MissingConfigValue('secret')
    if 'password' not in wordpress_section:
        raise MissingConfigValue('secret')


def test_search_console_config(config: configparser.ConfigParser) -> None:
    wordpress_section = config['searchconsole']
    if 'SCOPES' not in wordpress_section:
        raise MissingConfigValue('SCOPES')
    if 'ENDPOINT' not in wordpress_section:
        raise MissingConfigValue('ENDPOINT')
    if 'JSON_KEY_FILE' not in wordpress_section:
        raise MissingConfigValue('JSON_KEY_FILE')


def test_unsplash_config(config: configparser.ConfigParser) -> None:
    wordpress_section = config['unsplash']
    if 'accesskey' not in wordpress_section:
        raise MissingConfigValue('accesskey')
    if 'secretkey' not in wordpress_section:
        raise MissingConfigValue('secretkey')
