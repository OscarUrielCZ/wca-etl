from bs4 import BeautifulSoup
import requests

from etl.extract.competition import Competition
from etl.globals import BROWSER_HEADERS as headers
from etl.utils import build_url, get_href_and_text

def get_general_info():
    pass

def request_competition_data(url: str):
    comp = Competition(url)
    comp.get_general_info()
    
    if comp.has_results:
        print(comp.result_links)
    else:
        print('No results found')

def request_competition_links(year: int) ->  list[str]:
    competitions_url = f'https://www.worldcubeassociation.org/competitions?region=all&search=&year={year}&state=past&from_date=&to_date=&delegate=&display=list'

    response = requests.get(competitions_url, headers=headers)
    response.raise_for_status()

    html = BeautifulSoup(response.text, 'html.parser')

    competitions_items = html.select('#competitions-list .list-group-item.past')
    competitions_links = []

    # TODO: replace with util function
    for comp in competitions_items:
        comp_link = comp.select_one('.competition-link a')
        if comp_link and comp_link.has_attr('href'):
            comp_link = comp_link['href'].strip()
            competitions_links.append(build_url(comp_link))
            print(build_url(comp_link))
        
    return competitions_links