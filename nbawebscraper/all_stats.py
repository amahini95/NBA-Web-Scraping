import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

from nbawebscraper.data_src import get_soup, setup_data


def all_stats(season):
    """Get all NBA stats for all teams in a specific season
    
    Arguments:
        season {int} -- Seasons from 1947 - present (2022)
    """

    soup = get_soup()

    #Use .find() to search for tag & attributes for the first game
    pick_team = soup.find(name='div', attrs={'id': 'teams'})

    #make a list of url endings for all NBA team's websites
    teams = []
    #each team is in an "option" tag
    #the URL ending that we want is in the "value" attribute
    for option in pick_team.find_all('option')[1:31]:
        name = option.get('value')
        teams.append(name)

    #make a list of dicts to convert to a Pandas Dataframe
    nba_info = []

    #find url's for all NBA teams based on 'season'
    #also, make a BeautifulSoup object
    for team in teams:
        per_game = setup_data(team[-3:], season)

        #find all rows with 'tr', exclude the first row since it's the table's header
        for row in per_game.find_all('tr')[1:]:
            player = {}
            player['Name'] = row.find('a').text.strip()

            team = team[-3:]
            player['Team'] = team

            player['Name'] = row.find('a').text.strip()
            #print(row.find('a').text.strip())
            player['Age'] = row.find('td', {'data-stat': 'age'}).text
            player['Min PG'] = row.find('td', {'data-stat': "mp_per_g"}).text
            player['FG %'] = row.find('td', {'data-stat': 'fg_per_g'}).text
            player['Rebounds PG'] = row.find('td', {
                'data-stat': 'trb_per_g'
            }).text
            player['Assists PG'] = row.find('td', {
                'data-stat': 'ast_per_g'
            }).text
            player['Steals PG'] = row.find('td', {
                'data-stat': 'stl_per_g'
            }).text
            player['Blocks PG'] = row.find('td', {
                'data-stat': 'blk_per_g'
            }).text
            player['TO PG'] = row.find('td', {'data-stat': 'tov_per_g'}).text
            player['PPG'] = row.find('td', {'data-stat': 'pts_per_g'}).text

            player_url = ('https://www.basketball-reference.com/' +
                          row.find('a').attrs['href'])
            #Make a new BS instance of the players' page to narrow it down to the top section
            player_req = requests.get(player_url)
            player_soup = BeautifulSoup(player_req.content, 'lxml')
            player_info = player_soup.find(
                name='div', attrs={'itemtype': 'https://schema.org/Person'})
            '''
            #Making a list of hyperlinks from player_info
            player_links = []
            for link in player_info.find_all('a'):
                player_links.append(link.get('href'))

            #if a player is on Twitter, the link is second in player_links
            #else, it's listed as "No Twitter"
            if 'twitter' in player_links[1]:
                player['Twitter Handle'] = player_links[1].replace(
                    'https://twitter.com/', '')
            
            else:
                player['Twtitter Handle'] = 'No Twitter'
           
            Use RegEx to get heigh, weight, position from all players' own url's
            '(.*)' in RegEx lets us take text from 2 known substrings (think boundaries),
            where the substrings are placed on either side of '(.*)'
            '''
            #Makes a string of all the paragraph 'p' text from "player_info",
            #Which means s has all the weight, height, position info
            s = str(player_info.find_all('p'))
            weight = re.search('\"weight\">(.*)lb</span>', s)
            height = re.search(
                '\"height\">(.*)</span>,\xa0<span itemprop="weight', s)
            position = re.search('Position:\n  </strong>\n (.*)\n\n', s)

            if weight is None:
                player['Weight (Lbs)'] = 'N/A'
            else:
                player['Weight (Lbs)'] = weight.group(1).strip()

            if height is None:
                player['Height'] = 'N/A'
            else:
                player['Height'] = height.group(1).strip()

            if position is None:
                player['Position'] = 'N/A'
            else:
                player['Position'] = position.group(1).strip()

            nba_info.append(player)

    nba_info_df = pd.DataFrame(nba_info)
    return nba_info_df