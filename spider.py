# Spider class will grab one of the links from the waiting list and grab links off that site and add to waiting list
# Will also move links from waiting list to the crawled file
# Must share waiting list and crawled files among multiple spiders

from urllib.request import urlopen
from Web_Crawler.link_finder import LinkFinder
from Web_Crawler.general import *
from bs4 import BeautifulSoup


class Spider:

    # Class variables, shared among all instances of spiders
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name                      # All spiders are going to have this shared info
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First Spider', Spider.base_url)


    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)


    # Crawl the web page, updates user display
    @staticmethod
    def crawl_page(thread_name, page_url):
        if Spider.check_for_table(page_url) is False:
            return
        if page_url not in Spider.crawled:                  # make sure page has not already been crawled
            print(thread_name, 'now crawling', page_url)
            print('Queue ', str(len(Spider.queue)) + ' | Crawled ', str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()


    # Crawl page_url and return a set of links
    @staticmethod
    def gather_links(page_url):
        html_string = Spider.connect(page_url)
        if html_string is None:
            return set()                                        # if there is an error return an empty set
        finder = LinkFinder(Spider.base_url, page_url)
        finder.feed(html_string)                                # pass in html data
        return finder.page_links()                              # if there is no error return the set of page links


    # Takes a set of links and adds to already existing waiting list
    @staticmethod
    def add_links_to_queue(links):
        for url in links:                           # need to make sure not in waiting list and not in crawled list
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:       # prevent from crawling entire internet
                continue
            Spider.queue.add(url)


    # Updates the files
    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)


    # Check for tables in web page
    @staticmethod
    def check_for_table(page_url):
            html_string = Spider.connect(page_url)
            if html_string is None:
                return False
            soup = BeautifulSoup(html_string, 'html.parser')
            table_tags = soup.find_all('table')
            if not table_tags:
                return False
            return True


    # Make sure there is a valid connection
    @staticmethod
    def connect(page_url):
        try:
            response = urlopen(page_url)                            # connect to a web page
            if 'text/html' in response.getheader('Content-Type'):   # make sure you are connecting to a html page
                html_bytes = response.read()                        # reads in raw response in bytes
                html_string = html_bytes.decode('utf-8')            # convert bytes to UTF-8
                return html_string
        except Exception as e:
            print('Error: ', str(e), 'can not crawl page')
            return None

