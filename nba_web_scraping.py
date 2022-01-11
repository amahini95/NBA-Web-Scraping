#https://medium.com/analytics-vidhya/web-scraping-nba-data-with-pandas-beautifulsoup-and-regex-pt-2-fa0e4c1a16fa
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

#import seaborn as sns
#import matplotlib.pyplot as plt


#TODO: allow for team url input
def gsw_player_stats():

    #extract stats for 2021-22 GSW
    gsw_url = (f'https://www.basketball-reference.com/teams/GSW/2022.html')

    #requests lib sends 'GET' request to url
    gsw_req = requests.get(gsw_url)

    #parse content of HTML doc with bs4
    gsw_soup = BeautifulSoup(gsw_req.content, 'lxml')

    #Use .find() to search for tag & attributes for the first game
    gsw_per_game = gsw_soup.find(name='table', attrs={'id': 'per_game'})

    # Make a list of dicts (dict = player, key = stat category, val = value for cat)
    gsw_stats = []

    #find all rows with 'tr', exclude the first row since it's the header <thead>
    #which means we'll start at the <tbody>
    for row in gsw_per_game.find_all('tr')[1:]:

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
        gsw_stats.append(player)

    return pd.DataFrame(gsw_stats)


def get_gsw_twitter():

    #extract stats for 2021-22 GSW
    gsw_url = (f'https://www.basketball-reference.com/teams/GSW/2022.html')

    #requests lib sends 'GET' request to url
    gsw_req = requests.get(gsw_url)

    #parse content of HTML doc with bs4
    gsw_soup = BeautifulSoup(gsw_req.content, 'lxml')

    #Use .find() to search for tag & attributes for the first game
    gsw_per_game = gsw_soup.find(name='table', attrs={'id': 'per_game'})

    #Loop through players, make a list of dicts again
    #This time, retrieve Twitter handle
    twitter_handles = []

    for row in gsw_per_game.find_all('tr')[1:]:

        player = {}
        #Grab row's first hyperlink (player's url ending)
        #Append it to base url in order to get players' webpage url
        player_url = ('https://www.basketball-reference.com/' +
                      row.find('a').attrs['href'])

        #Make a new BS instance of the players' page to narrow it down to the top section
        player_req = requests.get(player_url)
        player_soup = BeautifulSoup(player_req.content, 'lxml')
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

        else:
            player['Twtitter Handle'] = 'No Twitter'

        twitter_handles.append(player)

    return pd.DataFrame(twitter_handles)


def get_h_w_p():

    #extract stats for 2021-22 GSW
    gsw_url = (f'https://www.basketball-reference.com/teams/GSW/2022.html')

    #requests lib sends 'GET' request to url
    gsw_req = requests.get(gsw_url)

    #parse content of HTML doc with bs4
    gsw_soup = BeautifulSoup(gsw_req.content, 'lxml')

    #Use .find() to search for tag & attributes for the first game
    gsw_per_game = gsw_soup.find(name='table', attrs={'id': 'per_game'})
    #Get heigh, weight and position
    height_weight_position = []

    for row in gsw_per_game.find_all('tr')[1:]:

        player = {}
        #Grab row's first hyperlink (player's url ending)
        #Append it to base url in order to get players' webpage url
        player_url = ('https://www.basketball-reference.com/' +
                      row.find('a').attrs['href'])

        #Make a new BS instance of the players' page to narrow it down to the top section
        player_req = requests.get(player_url)
        player_soup = BeautifulSoup(player_req.content, 'lxml')
        player_info = player_soup.find(
            name='div', attrs={'itemtype': 'https://schema.org/Person'})

        # Adding players' names, to go along with new stats
        player['Name'] = row.find('a').text.strip()
        '''
        Use RegEx to get heigh, weight, position from all players' own url's
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
        #print(position.group(1))

        height_weight_position.append(player)

    return pd.DataFrame(height_weight_position)


def get_all_gsw_stats():

    #extract stats for 2021-22 GSW
    gsw_url = (f'https://www.basketball-reference.com/teams/GSW/2022.html')

    #requests lib sends 'GET' request to url
    gsw_req = requests.get(gsw_url)
    #parse content of HTML doc with bs4
    gsw_soup = BeautifulSoup(gsw_req.content, 'lxml')

    #Use .find() to search for tag & attributes for the first game
    gsw_per_game = gsw_soup.find(name='table', attrs={'id': 'per_game'})

    # Make a list of dicts (dict = player, key = stat category, val = value for cat)
    gsw_info = []

    #find all rows with 'tr', exclude the first row since it's the header <thead>
    #which means we'll start at the <tbody>
    for row in gsw_per_game.find_all('tr')[1:]:

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
        '''
        #Use RegEx to get heigh, weight, position from all players' own url's
        #'(.*)' in RegEx lets us take text from 2 known substrings (think boundaries),
        #where the substrings are placed on either side of '(.*)'

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

        gsw_info.append(player)

    return pd.DataFrame(gsw_info)


def all_teams(year):

    base_url = 'https://www.basketball-reference.com/'

    #requests lib sends 'GET' request to url
    base_req = requests.get(base_url)

    #parse content of HTML doc with bs4
    base_soup = BeautifulSoup(base_req.content, 'lxml')

    #Use .find() to search for tag & attributes for the first game
    pick_team = base_soup.find(name='div', attrs={'id': 'teams'})

    #make a list of url endings for all NBA team's websites
    teams = []
    for i in pick_team.find_all('option')[1:31]:
        name = i.get('value')
        teams.append(name)

    #make a list of dicts to convert to a Pandas Dataframe
    nba_info = []

    #find url's for all NBA teams based on 'year'
    #also, make a BeautifulSoup object
    for i in teams:
        team_url = (
            f'https://www.basketball-reference.com{i}/{str(year)}.html')
        team_req = requests.get(team_url)
        team_soup = BeautifulSoup(team_req.content, 'lxml')
        per_game = team_soup.find(name='table', attrs={'id': 'per_game'})

        #find all rows with 'tr', exclude the first row since it's the table's header
        for row in per_game.find_all('tr')[1:]:
            player = {}
            player['Name'] = row.find('a').text.strip()

            team = i[-3:]
            player['Team'] = team

            player['Name'] = row.find('a').text.strip()
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

            player['Weight (Lbs)'] = weight.group(1).strip()
            player['Height'] = height.group(1).strip()
            player['Position'] = position.group(1).strip()

            nba_info.append(player)
            #print(player)

    nba_info_df = pd.DataFrame(nba_info)
    return nba_info_df


def obj_to_num(nba_df):
    #str_cols = ['Name', 'Team', 'Twitter', 'Position', 'Height']
    str_cols = ['Name', 'Team', 'Position', 'Height']

    for i in nba_df.columns:
        #print(i)
        if i not in str_cols:
            nba_df[i] = pd.to_numeric(nba_df[i])

    print(nba_df.dtypes)


if __name__ == "__main__":
    '''
    print(get_twitter_handles())
    print(get_h_w_p())
    '''

    all_nba_2022 = all_teams(2022)
    obj_to_num(all_nba_2022)
    '''
    gsw_df = get_all_gsw_stats()
    print(gsw_df)
    obj_to_num(gsw_df)
    '''

    #print(all_nba_2021[(all_nba_2022['Team'] == 'LAL')
    #                   & (all_nba_2022['FG %'] <= 0.40)])

    print(
        all_nba_2022.groupby('Team')[['Weight (Lbs)']].sum().sort_values(
            by='Weight (Lbs)', ascending=True).head(10))
    '''
    print(sns.histplot(all_nba_2022['Min PG'], bins=20))
    print(
        plt.title(
            'Frequency of Minutes Played Per Game in 2021 Across the NBA'))
    '''