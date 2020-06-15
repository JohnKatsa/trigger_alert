import time, sys

import preprocess as pre
import download as dow
import diff_checker as dc

THRESHOLD = 0.9
INTERVAL = 2

class page_checker:
    def __init__(self):
        self.url = 'http://johnkatsa.github.io/'
        self.preprocessor = pre.preprocess()
        self.downloader = dow.download()
        self.diff_checker = dc.diff_checker()

    # downloads and preprocesses
    def get(self) -> str:
        return self.preprocessor.preprocess_page(self.downloader.download_page(self.url))

    # refreshes page and checks differencies
    def refresh_page(self):
        new_content = self.get()            # get new page
        if(self.check(new_content)):        # check for differencies
            self.notify()
        self.page_content = new_content     # print result

    def check_and_update(self, counter: int):
        i = 0
        self.page_content = self.get()

        while(i < counter):
            time.sleep(INTERVAL)

            if(services.is_time_to_check(self.url)):
                self.refresh_page()
            i += 1

    def check(self, new_content: str) -> bool:
        return self.diff_checker.cosine(self.diff_checker.tf_idf(self.page_content, new_content)) < THRESHOLD

    def notify(self):
        print(self.url, "Changed")

if __name__ == "__main__":
    program = page_checker()
    program.check_and_update(int(sys.argv[1]))