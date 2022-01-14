import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import argparse

from nbawebscraper.all_stats import all_stats
from nbawebscraper.player_stats import player_stats
from nbawebscraper.player_twitter import get_twitter
from nbawebscraper.player_personal import get_personal_info


def main():
    """ Main entry point of the app """

    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str)
    parser.add_argument('--season', type=int, default=2022)
    parser.add_argument('--team', type=str, default="GSW")
    args = parser.parse_args()

    commands = {
        "all": lambda _, season: all_stats(season),
        "player": player_stats,
        "twitter": get_twitter,
        "personal": get_personal_info
    }

    if args.command in commands:
        print(commands[args.command](args.team, args.season))


if __name__ == "__main__":
    main()