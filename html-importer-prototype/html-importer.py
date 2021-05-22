from bs4 import BeautifulSoup
from requests_html import HTMLSession

import re

# Gets the HTML of ATel #13000
url = 'https://www.astronomerstelegram.org/?read=13000'
session = HTMLSession()

request = session.get(url)
request.html.render()

# Parses HTML to a tree
soup = BeautifulSoup(request.html.raw_html,'html.parser')

# ATel Number
print('ATel Number:\n' + re.search('[0-9]+', url).group() + '\n\n')

# ATel Title
print('Title:\n' + soup.find('h1', {'class': 'title'}).get_text(strip=True) + '\n\n')

# Authors of ATel
print('Authors:\n' + soup.find('strong').get_text(strip=True) + '\n\n')

# ATel Submission Time
print('Report Submission Time:')

elements = soup.find_all('strong')
print(elements[1].get_text(strip=True) + '\n\n')

# ATel Body
print('Body:')

texts = soup.find_all('p', {'class': None, 'align': None})
body = ''

for text in texts:
    if((text.find('iframe') == None) and (len(text.get_text(strip=True)) != 0) and (text.find('a') == None)):
        body += text.get_text(strip=True) + '\n\n'

print(body.strip() + '\n\n')

# Subjects Referred to by ATel
print('Subjects:')

subjects = soup.find('p', {'class': 'subjects'}).get_text().replace('Subjects: ', '').split(', ')

for subject in subjects:
    print(subject)

# Related ATel Links
print('\n\nRelated ATel Report Links:')

related_reports = []
string = 'https://www.astronomerstelegram.org/?read='
links = soup.find_all('a', href=True)

for link in links:
    if((link['href'].find(string) != -1) and (link['href'] != string) and (link.get_text() != 'Previous') and (link.get_text() != 'Next')):
        related_reports.append(link['href'])

related_reports = list(dict.fromkeys(related_reports))

for related_report in related_reports:
    print(related_report)

# Closes connection
session.close()
