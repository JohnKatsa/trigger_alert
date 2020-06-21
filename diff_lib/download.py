import requests

class download:
    def download_page(self, url, page_id, is_multi_page=False) -> str:
        text = ""
        kw = '&' if '?' in url else '?'
        
        if(is_multi_page):
            for i in range(1, 4):
                text += " " + requests.get(url + kw + page_id + '=' + str(i)).text
        else:
            text = requests.get(url).text

        return text