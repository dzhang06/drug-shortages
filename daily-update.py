from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
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
    df.sort_values(by='Revision Date', inplace=True, ascending=False)
    filtered_df = df[df['Revision Date'] >= date]
    return filtered_df


MASTER_URL = 'https://www.ashp.org/Drug-Shortages/Current-Shortages/Drug-Shortages-List?page=All'
today = datetime.now().strftime('%Y-%m-%d')
today_updates = get_updates(MASTER_URL, today)
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
