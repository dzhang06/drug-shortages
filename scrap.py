from bs4 import BeautifulSoup
import requests
import lxml
import csv
import pandas as pd

# db = csv.writer(open('database.csv', 'w', newline=''))
# db.writerow(['name', 'status', 'date', 'link'])

url = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/Drug-Shortages-List?page=All'
url_prefix = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
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
links = table.find_all('a')
for link in links:
    url = url_prefix + link.get('href')
    urls.append(url)
df['links'] = urls
df.to_csv('pandas_db.csv', index=False)
