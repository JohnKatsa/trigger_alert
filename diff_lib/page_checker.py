import time, sys

import preprocess as pre
import download as dow
import diff_checker as dc
import requests, json, datetime

THRESHOLD = 0.9
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
    def get(self, url) -> str:
        return self.preprocessor.preprocess_page(self.downloader.download_page(url))

    def update_url_timer(self, has_changed, timer):
        if(timer == 0):
            timer = datetime.datetime.now().timestamp() 
        return timer + (1 if has_changed else -1) * WEIGHT * timer

    def api_call_for_contents(self, my_instance, all_instances):
        self.contents = json.loads(requests.get(API + '?page_checker_id={}&page_checkers={}'.format(my_instance, all_instances)).text)

    def api_call_for_link_change(self, db_id, url, new_content, timer):
        data = {
            'url' : url,
            'content' : new_content,
            'next_check' : timer
        }
        res = requests.post(API, data=data)

    def produce_kafka(self, topic):
        kafka_produce

    def get_timer(self, url):
        for item in self.contents:
            if(item['url'] == url):
                return item['next_check']

    def check_and_update(self, my_instance, all_instances):
        while(True):
            time.sleep(INTERVAL)

            # get urls
            self.api_call_for_contents(my_instance, all_instances)

            for content in self.contents:
                url = content['url']
                old_content = content['content']
                new_content = self.get(url)

                self.notify(content['id'], self.check(old_content, new_content), old_content, new_content, url, self.get_timer(url))
                break
            break


    def check(self, old_content, new_content: str) -> bool:
        return self.diff_checker.cosine(self.diff_checker.tf_idf(old_content, new_content)) < THRESHOLD

    def notify(self, db_id, has_changed, old_content, new_content, url, old_timer):
        #if(has_changed):
        #    self.produce_kafka(url)
        self.api_call_for_link_change(db_id, url, new_content, self.update_url_timer(has_changed, old_timer))


if __name__ == "__main__":
    program = page_checker()
    
    my_instance = int(sys.argv[1])
    all_instances = int(sys.argv[2])
    program.check_and_update(my_instance, all_instances)