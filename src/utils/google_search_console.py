from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from utils.configparser import parse_config
from pathlib import Path


class GoogleSearchConsole:

    def __init__(self, to_index_url: str):
        self.config = parse_config()
        self.url = to_index_url

    # TODO cache token
    def get_token(self) -> None:
        pass

    def send_index_request(self) -> None:
        scopes = self.config['search_console']['SCOPES']
        endpoint = self.config['search_console']['ENDPOINT']
        key_file_location = self.config['search_console']['JSON_KEY_FILE']
        filepath = Path(__file__).resolve().parents[2]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{filepath}/{key_file_location}",
                                                                       scopes=scopes)
        print(f"{filepath}/{key_file_location}")
        print(scopes)
        print(endpoint)
        http = credentials.authorize(httplib2.Http())

        content = """{{
                    "url": "{}",
                    "type": "URL_UPDATED"
                    }}""".format(self.url)

        response, content = http.request(endpoint, method="POST", body=content)
        print(response.reason)
