import re
from bs4 import BeautifulSoup

class preprocess:
    def preprocess_page(self, text: str) -> str:
        return self.soup_call(text)

    def soup_call(self, text: str) -> str:
        soup = BeautifulSoup(text, features="html.parser")
        print(" ".join(soup.get_text().split()))
        return " ".join(soup.get_text().split())
