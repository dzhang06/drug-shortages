from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


MASTER_URL = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/' \
             'Drug-Shortages-List?page=All'


def generate_list(url):
    """ generate new list from website """
    # db = csv.writer(open('database.csv', 'w', newline=''))
    # db.writerow(['name', 'status', 'date', 'link'])
    url = url
    url_prefix = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='lxml')
    # trs = soup.find_all('tr')
    # for tr in trs:
    #     tds = tr.find_all("td")
    #     try:
    #         names = str(tds[0].get_text())
    #         status = str(tds[1].get_text())
    #         revision_date = str(tds[2].get_text())
    #         link = url_prefix + tds[0].find('a').get('href')
    #     except:
    #         print("bad formatting: {}".format(tds))
    #         continue
    #
    #     db.writerow([names, status, revision_date, link])
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))[0]
    urls = []
    ids = []
    links = table.find_all('a')
    for link in links:
        url = url_prefix + link.get('href')
        urls.append(url)
        id = pass ######### NEED TO FIGURE OUT HOW TO EXTRACT PRODUCT ID FROM URL
    df['links'] = urls
    df['id'] = ids
    return df


def save_to_file(frame):
    """
    save the dataframe to file as csv
    """
    frame.to_csv('pandas_db.csv', index=False)


def generate_details(frame):
    """
    Loops through drug details page to get some important details
    of the drugs
    """
    pass


# primary_df = generate_list(MASTER_URL)
# save_to_file(primary_df)

primary_df = pd.read_csv('pandas_db.csv')


def get_details(df):
    """
    loop through each drug, get details from page, and add them to df
    Parameters
    ----------
    df : dataframe
        start with dataframe with only front page info only.

    Returns
    -------
    df : dataframe
        returns dataframe with all data inside.

    """


    def extract_details(url):
        pass

    
    example_url = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/Drug-Shortage-Detail.aspx?id=437'

    df = df
    for index, row in df.iterrows():
        url = row[3]
        extract_details(url)
    return df


df_2 = get_details(primary_df)
