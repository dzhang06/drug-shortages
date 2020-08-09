from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from datetime import datetime

# for testing short bits of code...

MASTER_URL = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/Drug-Shortages-List?page=All'


def get_updates(url, date):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))[0]
    df['Revision Date'] = pd.to_datetime(df['Revision Date'], format='%b %d, %Y')
    df.sort_values(by='Revision Date', inplace=True, ascending=False)
    print(df)
    filtered_df = df[df['Revision Date'] >= date]
    print(filtered_df)


date = datetime.strptime('2020-08-06', format('%Y-%m-%d'))
get_updates(MASTER_URL, date)
