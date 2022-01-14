import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import re

from nbawebscraper.data_src import setup_data


def get_twitter(name: str, season: int):
    """Get NBA players' Twitter handles for any team and any season
    
    Arguments:
        name {str} -- Name of player
        season {int} -- Seasons from 1947 - present (2022)
    """

    per_game = setup_data(name, season)

    if per_game is None:
        return None

    #Loop through players, make a list of dicts again
    #This time, retrieve Twitter handle
    twitter_handles = []

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

        # Adding players' names, to go along with Twitter page
        player['Name'] = row.find('a').text.strip()

        #Making a list of hyperlinks from player_info
        player_links = []
        for link in player_info.find_all('a'):
            player_links.append(link.get('href'))

        #if a player is on Twitter, the link is second in player_links
        #else, it's listed as "No Twitter"
        if 'twitter' in player_links[1]:
            player['Twitter Handle'] = player_links[1].replace(
                'https://twitter.com/', '')

        #BUG: If at least one player has no Twitter handle, "NaN" is returned
        #for that player and all other who are not on Twitter.
        #Potentially esolve this by returning "No Twitter" instead.
        #However, at the moment doing so results in creation of an
        # additional column (which is currently what happens when
        # trying to address this "No Twitter" scenario)

        #else:
        #    player['Twitter Handle'] = 'No Twitter'

        twitter_handles.append(player)

    return pd.DataFrame(twitter_handles)