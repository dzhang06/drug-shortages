from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# for testing short bits of code...

example_url = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/Drug-Shortage-Detail.aspx?id=437'
response = requests.get(example_url)
soup = BeautifulSoup(response.text, 'lxml')
date = soup.find_all('p', attrs={'class': 'date'})[0].span.text
drug = soup.find_all('h1', attrs={'class': 'alt'})[0].span.text
updated = soup.find_all('div', attrs={'id': '1_Updated'})[0].p.span.p.text

elements = ['1_Affected',
            '1_Reason',
            '1_Avaliable',  # apparently misspelled in code
            '1_Resupply',
            '1_Alternatives',
            '1_References']

products_affected = []
reason_shortage = []
available_product = []
est_resupply_date = []
alternative_agents_management = []
references = []


def extract_data(element):
    if element == '1_References':
        element_data = soup.find_all('div', attrs={'id': element})[0].ul.li.span.ol
    else:
        element_data = soup.find_all('div', attrs={'id': element})[0].ul.li.span.ul
    element_list = []
    for child in element_data.children:
        element_list.append(child.text)
    return element_list


for element in elements:
    print(extract_data(element))

# products = soup.find_all('div', attrs={'id': '1_Affected'})[0].ul.li.span.ul

# for child in products.children:
#     products_affected.append(child.text)
# print(child.text)
# print(products)
# print(products)
