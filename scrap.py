from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

MASTER_URL = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/Drug-Shortages-List?page=All'


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
        pattern = re.compile(r'id=(\d+)$')
        drug_id = re.search(pattern, url).group(1)
        ids.append(drug_id)
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



def get_details(shortage_df):
    """
    loop through each drug, get details from page, and add them to df
    Parameters
    ----------
    shortage_df : dataframe
        start with dataframe with only front page info only.

    Returns
    -------
    df : dataframe
        returns dataframe with all data inside.

    """

    def extract_each_drug(url, id, df):
        """
        Extract page details from URL
        List of:
            products_affected - list of products, mfg, ndc affected
            reason_shortage - reason for shortage of above products
            available_product - available products for ordering
            est_resupply_date - resupply date estimates
            alternative_agents_management - alternative options
            references - list of references
            updated - last updated date and information
        :param url: url of specific drug id
        :return - a tuple of page elements ? or dictionary:
        """
        products_affected = []
        reason_shortage = []
        available_product = []
        est_resupply_date = []
        alternative_agents_management = []
        references = []
        updated = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        drug_id = id
        date = soup.find_all('p', attrs={"class": "date"})[0].span.text
        drug = soup.find_all('h1', attrs={'class': 'alt'})[0].span.text
        updated = soup.find_all('div', attrs={'id': '1_Updated'})[0].p.span.p.text
        elements = ['1_Affected',
                    '1_Reason',
                    '1_Avaliable',  # apparently misspelled in code
                    '1_Resupply',
                    '1_Alternatives',
                    '1_References']

        def extract_data_pieces(element):
            exists = soup.find_all(id=element)
            if len(exists) > 0:
                if element == '1_References':
                    # element_data = soup.find_all('div', attrs={'id': element})[0].ul.li.span.ol
                    element_data = exists[0].ul.li.span.ol
                else:
                    # element_data = soup.find_all('div', attrs={'id': element})[0].ul.li.span.ul
                    element_data = exists[0].ul.li.span.ul
            else:
                element_data = None

            element_list = []
            if element_data is not None:
                for child in element_data.children:
                    element_list.append(child.text)
            return element_list
        example_url = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/Drug-Shortage-Detail.aspx?id=437'

        df = df
        for element in elements:
            lst = extract_data_pieces(element)
            for item in lst:
                df = df.append({'id': drug_id, 'drug': drug, 'type': element, 'data': item}, ignore_index=True)
        return df

    cols = ['id', 'drug', 'type', 'data']
    details_df = pd.DataFrame(columns=cols)
    loop = 1
    print(shortage_df)
    list_dfs = []
    # iterate through shortage drug list with unique ID and extract a df of drug properties
    for index, row in shortage_df.iterrows():
        url = row[3]
        drug_id = row[4]
        if pd.notna(url):
            print('completed loop: ', loop)
            list_dfs.append(extract_each_drug(url, drug_id, details_df))
            # details_df = details_df.append(drug_df, ignore_index=True)
        loop += 1
    details_df = pd.concat(list_dfs, ignore_index=True)
    return details_df


df_2 = get_details(primary_df)
df_2.to_csv('drugs.csv', index=False)
primary_df = pd.read_csv('pandas_db.csv')
details_df = pd.read_csv('drugs.csv')
