import configparser
from pathlib import Path


def parse_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    file = Path(__file__).resolve().parents[2]
    config.read(f'{file}/config.ini')
    return config
