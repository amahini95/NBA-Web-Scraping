from typing import Optional
from numpy import empty
import requests
from bs4 import BeautifulSoup as bs

BASE_URL = 'https://www.basketball-reference.com'


def get_soup(path="/") -> Optional[bs]:
    #extract stats for {name} in {season}

    url = BASE_URL + path

    try:
        #requests lib sends 'GET' request to url, allowing us to get data from 'url'
        req = requests.get(url)

        #Use BS to parse content of HTML doc with bs4, restructuring it so we can run more commands on it later
        soup = bs(req.content, 'lxml')

        return soup
    except Exception as e:
        print(e)
        return None


def setup_data(name: str, season: int):

    if len(name) != 3:
        raise ValueError("Team name must be 3 characters long")
    if season < 1947:
        raise ValueError(
            f"{season} is an invalid NBA year, available seasons are between 1947 - 2022"
        )

    soup = get_soup(f"/teams/{name.upper()}/{season}.html")

    #Use .find() to search for 'table' tag & id attribute of 'per_game' for the first game
    per_game = soup.find(name='table', attrs={'id': 'per_game'})

    return per_game