# NBA Web Scraping

Gathering NBA stats across any team and any season using Python, Pandas, BeautifulSoup, and RegEx

To run code
Go to the project's root directory, run the following command

python3 main.py [command] --season [year as an int in YYYY format] --team [team abbreviation in 3 capitals chars]
    
Where command is one of the following:
all: Retrieves all stats/player info across all teams in one season
player: Retrieves game stats for one team in one season
twitter: Retrieves one team's players' Twtiter handles
personal: Retrieves one team's players' height, weight and position

Running the command

python3 main.py [command]

will, by default, return the corresponding stats/info for the Golden State Warriors' 2021-2022 NBA regular season
