import re

from etl.globals import BASE_URL

is_well_formed_url = re.compile(r'^https?://.+/.+$')
is_relative_url = re.compile(r'^/.+$')

def build_url(url: str):
    if is_well_formed_url.match(url):
        return url
    elif is_relative_url.match(url):
        return  BASE_URL + url
    else:
        return BASE_URL + '/' + url
    
def get_href_and_text(a):
    link, text = None, None
    
    if a and a.has_attr('href'):
        link = a['href'].strip()
        text = a.text.strip()
    
    return link, text
