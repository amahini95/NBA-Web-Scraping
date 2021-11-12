import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

#extract stats for 2021-22 GSW
gsw_url = (f'https://www.basketball-reference.com/teams/GSW/2022.html')

#requests lib sends 'GET' request to url
gsw_res = requests.get(gsw_url)

#