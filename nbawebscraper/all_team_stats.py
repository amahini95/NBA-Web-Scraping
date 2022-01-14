import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import re

from nbawebscraper.data_src import setup_data


def get_all_stats(name: str, season: int):
    """Get NBA game stats for any team and any season
    
    Arguments:
        name {str} -- Name of player
        season {int} -- Seasons from 1947 - present (2022)
    """

    per_game = setup_data(name, season)

    if per_game is None:
        return None

    # Make a list of dicts (dict = player, key = stat category, val = value for cat)
    info = []

    #find all rows with 'tr', exclude the first row since it's the header <thead>
    #which means we'll start at the <tbody>
    for row in per_game.find_all('tr')[1:]:

        player = {}
        player['Name'] = row.find('a').text.strip()
        player['Age'] = row.find('td', {'data-stat': 'age'}).text
        player['Min PG'] = row.find('td', {'data-stat': "mp_per_g"}).text
        player['FG %'] = row.find('td', {'data-stat': 'fg_per_g'}).text
        player['Rebounds PG'] = row.find('td', {'data-stat': 'trb_per_g'}).text
        player['Assists PG'] = row.find('td', {'data-stat': 'ast_per_g'}).text
        player['Steals PG'] = row.find('td', {'data-stat': 'stl_per_g'}).text
        player['Blocks PG'] = row.find('td', {'data-stat': 'blk_per_g'}).text
        player['TO PG'] = row.find('td', {'data-stat': 'tov_per_g'}).text
        player['PPG'] = row.find('td', {'data-stat': 'pts_per_g'}).text

        player_url = ('https://www.basketball-reference.com/' +
                      row.find('a').attrs['href'])

        #Make a new BS instance of the players' page to narrow it down to the top section
        player_req = requests.get(player_url)
        player_soup = bs(player_req.content, 'lxml')
        player_info = player_soup.find(
            name='div', attrs={'itemtype': 'https://schema.org/Person'})

        #Making a list of hyperlinks from player_info
        player_links = []
        for link in player_info.find_all('a'):
            player_links.append(link.get('href'))

        #if a player is on Twitter, the link is second in player_links
        #else, it's listed as "No Twitter"
        if 'twitter' in player_links[1]:
            player['Twitter Handle'] = player_links[1].replace(
                'https://twitter.com/', '')
        '''
        Use RegEx to get heigh, weight, position from all players' own url's
        '(.*)' in RegEx lets us take text from 2 known substrings (think boundaries),
        where the substrings are placed on either side of '(.*)'

        Makes a string of all the paragraph 'p' text from "player_info",
        Which means s has all the weight, height, position info
        '''
        s = str(player_info.find_all('p'))
        weight = re.search('\"weight\">(.*)lb</span>', s)
        height = re.search('\"height\">(.*)</span>,\xa0<span itemprop="weight',
                           s)
        position = re.search('Position:\n  </strong>\n (.*)\n\n', s)

        player['Weight (Lbs)'] = weight.group(1).strip()
        player['Height'] = height.group(1).strip()
        player['Position'] = position.group(1).strip()

        info.append(player)

    return pd.DataFrame(info)