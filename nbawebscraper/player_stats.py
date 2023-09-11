import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import re

from nbawebscraper.data_src import setup_data


def player_stats(name: str, season: int):
    """Get NBA game stats for any team and any season
    
    Arguments:
        name {str} -- Name of player
        season {int} -- Seasons from 1947 - present (2022)
    """

    per_game = setup_data(name, season)

    if per_game is None:
        return None

    # Make a list of dicts (each dict = 1 player, key = stat category, val = value for cat),
    # serves as the pandas dataframe returned at the end
    stats = []
    '''
    Each player's stats are found row by row in 'per_game' table, 
    so find all rows with 'tr'.
    Exclude the first row since it's the header title <thead>,
    which means we'll start at <tbody>
    '''
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
        stats.append(player)

    #finally convert list of dicts to a pandas dataframe
    return pd.DataFrame(stats)