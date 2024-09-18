from bs4 import BeautifulSoup
import requests

from etl.globals import BROWSER_HEADERS as headers
from etl.utils import get_href_and_text

class Competition():
    name: str
    date: str
    city: str
    venue: str
    address: str
    organizers: list
    delegates: list

    def __init__(self, url) -> None:
        self._url = url
        self.__get_page_body()

    def __get_page_body(self) -> None:
        response = requests.get(self._url, headers=headers)
        response.raise_for_status()

        self._html = BeautifulSoup(response.text, 'html.parser')

    def get_general_info(self) -> None:
        name_elem = self._html.select_one('#competition-data h3')
        self.name = name_elem.text.strip() if name_elem else None

        info_items = self._html.select('#competition-data .competition-info .col-md-6:first-child dd')
        
        if len(info_items) > 0:
            self.date = info_items[0].text.strip()
            self.city = info_items[1].text.strip()
            self.venue = info_items[2].text.strip()
            self.address = info_items[3].text.strip()
            self.organizers = self._extract_links(info_items[6])
            self.delegates = self._extract_links(info_items[7])

        print(self.name, self.date, self.city, self.venue, self.address, self.organizers, self.delegates)

    def _extract_links(self, elem) -> list:
        return list(map(get_href_and_text, elem.select('a')))
    

    
