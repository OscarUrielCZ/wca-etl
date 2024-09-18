from dataclasses import dataclass

class Competition():
    name: str
    link: str
    date: str
    avenue: str
    address: str
    def __init__(self, url: str):
        self._url = url

    @property
    def url(self):
        return self._url

    

    
