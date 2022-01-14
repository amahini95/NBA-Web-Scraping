import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import re

from nbawebscraper.data_src import setup_data


def get_personal_info(name: str, season: int):
    """Get NBA players' personal info for any team and any season
    
    Arguments:
        name {str} -- Name of player
        season {int} -- Seasons from 1947 - present (2022)
    """

    per_game = setup_data(name, season)

    if per_game is None:
        return None

    #Get heigh, weight and position
    height_weight_position = []

    for row in per_game.find_all('tr')[1:]:

        player = {}
        #Grab row's first hyperlink (player's url ending)
        #Append it to base url in order to get players' webpage url
        player_url = ('https://www.basketball-reference.com/' +
                      row.find('a').attrs['href'])

        #Make a new BS instance of the players' page to narrow it down to the top section
        player_req = requests.get(player_url)
        player_soup = bs(player_req.content, 'lxml')
        player_info = player_soup.find(
            name='div', attrs={'itemtype': 'https://schema.org/Person'})

        # Adding players' names, to go along with new stats
        player['Name'] = row.find('a').text.strip()
        '''
        Use RegEx to get height, weight, position from all players' own url's
        '(.*)' in RegEx lets us take text from 2 known substrings (think boundaries),
        where the substrings are placed on either side of '(.*)'
        '''
        #Makes a string of all the paragraph 'p' text from "player_info",
        #Which means s has all the weight, height, position info
        s = str(player_info.find_all('p'))
        weight = re.search('\"weight\">(.*)lb</span>', s)
        height = re.search('\"height\">(.*)</span>,\xa0<span itemprop="weight',
                           s)
        position = re.search('Position:\n  </strong>\n (.*)\n\n', s)

        player['Weight (Lbs)'] = weight.group(1).strip()
        player['Height'] = height.group(1).strip()
        player['Position'] = position.group(1).strip()

        height_weight_position.append(player)

    return pd.DataFrame(height_weight_position)