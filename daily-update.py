from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config


def get_updates(url, date):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))[0]
    df['Revision Date'] = pd.to_datetime(df['Revision Date'], format='%b %d, %Y')
    url_prefix = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/'
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

    df.sort_values(by='Revision Date', inplace=True, ascending=False)
    filtered_df = df[df['Revision Date'] >= date]
    filtered_df = filtered_df.drop(columns=['Shortage Status', 'id'])
    return filtered_df


MASTER_URL = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/Drug-Shortages-List?page=All'
today = datetime.now().strftime('%Y-%m-%d')
today_updates = get_updates(MASTER_URL, today)
# print(today_updates)


s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(config.username, config.password)
message = MIMEMultipart()
message['Subject'] = 'Drug Shortage update for ' + today
message['From'] = 'dzpynotifier@gmail.com'
html = """\
<html>
    <head></head>
    <body>
        {0}
    </body>
</html>
""".format(today_updates.to_html(index=False).replace('border="1"', 'border="0"'))
part1 = MIMEText(html, 'html')
message.attach(part1)
s.sendmail('dzpynotifier@gmail.com', 'dzhang06@gmail.com', message.as_string())
s.quit()
