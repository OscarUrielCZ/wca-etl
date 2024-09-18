from etl.extract.scraper import (
    request_competition_links, 
    request_competition_data
    )

competition_year = 2024

url1 = 'https://www.worldcubeassociation.org/competitions/BarbertonMini22024'
url2 = 'https://www.worldcubeassociation.org/competitions/AudentesOpen2024'

request_competition_data(url1)
# request_competition_links(competition_year)





