import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


# Path setup
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)


def scrape_draft_class(year):
    url = f"https://www.basketball-reference.com/draft/NBA_{year}.html"

    response = requests.get(url)  # Fetches the raw html
    time.sleep(3)  # Adds 3 seconds between requests to respect rate limits (prevents getting blocked by site)

    soup = BeautifulSoup(response.content, 'html.parser')  # Html gets parsed into a navigable structure
    table = soup.find('table', id='stats')  # Find specific table

    # Read with multi-level header
    df = pd.read_html(str(table), header=[0, 1])[0]

    # Flatten column names cleanly
    df.columns = [col[1] if 'Unnamed' in col[0] else '_'.join(col).strip()
                  for col in df.columns]

    return df


# Creates a folder for raw data if it doesn't already exist
os.makedirs(os.path.join(base_dir, 'data', 'raw'), exist_ok=True)

draft_classes = []

# Range of draft years to be scraped
for year in range(2008, 2021):
    print(f"Scraping {year} draft class...")
    df = scrape_draft_class(year)
    df['draft_year'] = year
    draft_classes.append(df)

all_drafts = pd.concat(draft_classes, ignore_index=True)
all_drafts.to_csv(os.path.join(base_dir, 'data', 'raw', 'draft_raw.csv'), index=False)
print(f"Done. Saved {len(all_drafts)} rows.")
