import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_draft_class(year):
    url = f"https://www.basketball-reference.com/draft/NBA_{year}.html"

    response = requests.get(url)    # Fetches the raw html
    time.sleep(3)   # Adds 3 seconds between requests to respect rate limits (prevents getting blocked by site)

    soup = BeautifulSoup(response.content, 'html.parser')   # Html gets parsed into a navigable structure
    table = soup.find('table', id='stats')  # Find specific table

    return pd.read_html(str(table))[0]  # Pandas reads HTML table cleanly

draft_classes = []
for year in range(2010, 2022):
    df = scrape_draft_class(year)
    df['draft year'] = year
    draft_classes.append(df)

all_drafts = pd.concat(draft_classes, ignore_index=True)

