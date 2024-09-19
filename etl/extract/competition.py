from bs4 import BeautifulSoup
import requests

from etl.extract.href import Href
from etl.globals import BROWSER_HEADERS as headers
from etl.utils import build_url, get_href_and_text

class Competition():
    name: str
    date: str
    city: str
    venue: str
    address: str
    organizers: list
    delegates: list
    result_links: dict = {}

    def __init__(self, url) -> None:
        self._url = url
        self.__get_page_body()

    def get_general_info(self) -> None:
        self.__get_competition_name()
        self.__get_competition_info()
        self.__get_menu_links()

    @property
    def has_results(self) -> bool:
        return 'podiums' in self.result_links

    def __convert_links_to_competitor(self, links: list[tuple[str, str]]) -> list:
        competitors: list[Href] = []

        for link in links:
            href = build_url(link[0])
            text = link[1]
            competitors.append(Href(href, text))

        return competitors

    def __extract_links(self, elem) -> list:
        return list(map(get_href_and_text, elem.select('a')))
    
    def __get_competition_info(self) -> None:
        info_items = self._html.select('#competition-data .competition-info .col-md-6:first-child dd')
        if len(info_items) > 0:
            self.date = info_items[0].text.strip()
            self.city = info_items[1].text.strip()
            self.venue = info_items[2].text.strip()
            self.address = info_items[3].text.strip()
            self.organizers = self.__convert_links_to_competitor(self.__extract_links(info_items[6]))
            self.delegates = self.__convert_links_to_competitor(self.__extract_links(info_items[7]))

    def __get_competition_name(self) -> None:
        name_elem = self._html.select_one('#competition-data h3')
        self.name = name_elem.text.strip() if name_elem else None

    def __get_menu_links(self) -> None:
        menu_items = self._html.select('#competition-nav .list-group-item')

        if not menu_items or len(menu_items) == 0:
            return

        menu_items = list(map(get_href_and_text, menu_items))
        for item in menu_items:
            if item[1].lower() == 'podiums':
                self.result_links['podiums'] = build_url(item[0])
            elif item[1].lower() == 'all':
                self.result_links['all'] = build_url(item[0])
            elif item[1].lower() == 'by person':
                self.result_links['competitors'] = build_url(item[0])
            elif item[1].lower() == 'scrambles':
                self.result_links['scrambles'] = build_url(item[0])
    
    def __get_page_body(self) -> None:
        response = requests.get(self._url, headers=headers)
        response.raise_for_status()

        self._html = BeautifulSoup(response.text, 'html.parser')
    
