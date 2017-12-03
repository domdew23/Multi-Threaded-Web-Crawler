# Responsible for extracting the domain name
# Only stick to links from one domain, not the entire internet

from urllib.parse import urlparse


# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')   # creates a list of domain elements
        return results[-2] + '.' + results[-1]          # return second to last.last element
    except:
        return 'get_domain_name failed'


# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc     # parse url and return the network  location
    except:
        return 'get_sub_domain_name failed'

