import requests

class download:
    def download_page(self, url: str) -> str:
        return requests.get(url).text