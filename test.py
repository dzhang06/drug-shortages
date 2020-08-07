from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# for testing short bits of code...

example_url = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/Drug-Shortage-Detail.aspx?id=437'
response = requests.get(example_url)
soup = BeautifulSoup(response.text, 'lxml')
date = soup.find_all('p', attrs={"class": "date"})[0].span.text
drug = soup.find_all('h1', attrs={'class': 'alt'})[0].span.text
updated = soup.find_all('div', attrs={'id': '1_Updated'})[0].p.span.p.text

products_affected = []
products = soup.find_all('div', attrs={'id': '1_Affected'})[0]
print(products)
print(products.div.h3)