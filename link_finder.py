# Class is going to get all of the links from an html page
from html.parser import HTMLParser
from urllib import parse
from bs4 import BeautifulSoup
import requests


class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()                        # when you start crawling links store in links set

    def handle_starttag(self, tag, attrs):
        if tag == 'a':                                         # start tag when you come across an anchor tag
            for (attribute, value) in attrs:                   # creates a tuple for each attribute in the anchor
                if attribute == 'href':                        # when you come across href attribute
                    url = parse.urljoin(self.base_url, value)  # when you come across a relative url, add homepage url
                    self.links.add(url)                        # url  will be properly formatted when added to set

    def page_links(self):
        return self.links

    def error(self, message):
        pass


'''
finder = LinkFinder()
finder.feed('<html><head><title>Test</title></head>'
            '<body><h1>Parse me!</h1></body></html>')  # feed function takes in html code
'''