import time, sys

import preprocess as pre
import download as dow
import diff_checker as dc
import requests, json, datetime

THRESHOLD = 0.97
INTERVAL = 1
WEIGHT = 0.1
API = 'http://localhost:8000/links/all/'

class page_checker:
    def __init__(self):
        self.preprocessor = pre.preprocess()
        self.downloader = dow.download()
        self.diff_checker = dc.diff_checker()
        self.contents = []

    # downloads and preprocesses
    def get(self, url, page_id) -> str:
        return self.preprocessor.preprocess_page(self.downloader.download_page(url, page_id))

    def update_url_timer(self, has_changed, timer, penalty):
        if(timer == 0):
            timer = datetime.datetime.now().timestamp()
        print(has_changed) 
        penalty = penalty + (-1 if has_changed else 1)*penalty*WEIGHT
        return datetime.datetime.now().timestamp() + penalty, penalty

    def api_call_for_contents(self, my_instance, all_instances):
        self.contents = json.loads(requests.get(API + '?page_checker_id={}&page_checkers={}'.format(my_instance, all_instances)).text)

    def api_call_for_link_change(self, db_id, url, old_content, new_content, timer, penalty, has_changed, version):
        data = {
            'id' : db_id,
            'url' : url,
            'content' : new_content if has_changed else old_content,
            'next_check' : timer,
            'penalty' : penalty,
        }
        if has_changed:
            data['version'] = version+1
        else:
            data['version'] = version
        res = requests.post(API, data=data)

    def get_timer(self, url):
        for item in self.contents:
            if(item['url'] == url):
                return item['next_check']

    def check_and_update(self, my_instance, all_instances):
        while(True):
            time.sleep(INTERVAL)

            # get urls
            self.api_call_for_contents(my_instance, all_instances)

            print([c['url'] for c in self.contents])

            for content in self.contents:
                url = content['url']
                version = int(content['version'])
                old_content = content['content']
                page_id = content['page_id']
                new_content = self.get(url, page_id)
                penalty = float(content['penalty'])

                self.notify(content['id'], self.check(old_content, new_content), old_content, new_content, url, self.get_timer(url), penalty, version)


    def check(self, old_content, new_content: str) -> bool:
        return self.diff_checker.cosine(self.diff_checker.tf_idf(old_content, new_content)) < THRESHOLD

    def notify(self, db_id, has_changed, old_content, new_content, url, old_timer, penalty, version):
        timer, penalty = self.update_url_timer(has_changed, old_timer, penalty)
        self.api_call_for_link_change(db_id, url, old_content, new_content, timer, penalty, has_changed, version)


if __name__ == "__main__":
    program = page_checker()
    
    my_instance = int(sys.argv[1])
    all_instances = int(sys.argv[2])
    program.check_and_update(my_instance, all_instances)