import requests

class download:
    def download_page(self, url, is_multi_page=False) -> str:
        text = ""
        
        if(is_multi_page):
            for i in range(1, 4):
                text += " " + requests.get(url + str(i)).text
        else:
            text = requests.get(url).text

        return text