import requests
from requests.exceptions import HTTPError   # for checking HTTP errors
from urllib.parse import urljoin
from logging import getLogger
from pathlib import Path

log = getLogger(__name__)


class KeggAPI:
    BASE: str = "https://rest.kegg.jp/"

    def api_request(self, *args) -> requests.Response:
        url_string = '/'.join(args)
        url: str = self.__join_url(self.BASE, url_string)
        log.critical(f"URL: {url}")
        response = requests.get(url)
        return self.__handle_response(response)

    def link(self, __feature, __value) -> requests.Response:
        return self.api_request('link', __feature, __value)

    def list(self, __value) -> requests.Response:
        return self.api_request('list', __value)

    def find(self, __value) -> requests.Response:
        return self.api_request('find', __value)

    def get(self, __feature, __value, *args) -> requests.Response:
        return self.api_request('get', __value, *args)


    @staticmethod
    def __join_url(*args) -> str:
        return urljoin(*args)

    @staticmethod
    def __handle_response(response: requests.Response) -> requests.Response:
        if response.status_code == 200:
            return response
        else:
            raise HTTPError(f"Error: {response.status_code}")