import requests
from bs4 import BeautifulSoup as bs


def setup_data(name: str, season: int):

    if len(name) != 3:
        raise ValueError("Team name must be 3 characters long")
    if season < 1947:
        raise ValueError(
            f"{season} is an invalid NBA year, available seasons are between 1947 - 2022"
        )

    #extract stats for {name} in {season}
    url = (
        f'https://www.basketball-reference.com/teams/{name.upper()}/{season}.html'
    )

    #requests lib sends 'GET' request to url
    req = requests.get(url)

    #parse content of HTML doc with bs4
    soup = bs(req.content, 'lxml')

    #Use .find() to search for tag & attributes for the first game
    per_game = soup.find(name='table', attrs={'id': 'per_game'})

    return per_game