import threading
from queue import Queue
from Web_Crawler.spider import Spider
from Web_Crawler.domain import *
from Web_Crawler.general import *


# A thread allows to split up jobs

# write in all caps to specify constant
# CONSTANTS:
PROJECT_NAME = 'fantasydata'
HOMEPAGE = 'https://fantasydata.com/nfl-stats/nfl-fantasy-football-stats.aspx'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8


queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)   # create a new thread
        t.daemon = True                       # ensures it will die when main exits
        t.start()

# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)  # assign job to new thread
        queue.task_done()

# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()                                                # ensures threads don't collide
    crawl()


# Check if their are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)                      # convert links in the file to a set
    if len(queued_links) > 0:                                   # check if there are links to be crawled
        print(str(len(queued_links)), ' links in the queue')
        create_jobs()


create_workers()
crawl()