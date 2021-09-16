from bs4 import BeautifulSoup
from requests_html import HTMLSession

import re

atel_nums = [10000, 11000, 12000, 13000, 14000]
session = HTMLSession()

# Testing done using 5 ATel reports
for atel_num in atel_nums:
    url = f'https://www.astronomerstelegram.org/?read={atel_num}'

    request = session.get(url)
    request.html.render(timeout=20)

    soup = BeautifulSoup(request.html.raw_html, 'html.parser')

    # Extracts subjects
    subjects = []

    if(soup.find('p', {'class': 'subjects'}) is not None):
        subjects = soup.find('p', {'class': 'subjects'}).get_text()
    
    print(f'{atel_num}: {subjects}')
    
    # Extracts referred by ATel numbers
    referred_by_nums = []

    if(soup.find('div', {'id': 'references'}) is not None):
        referred_by = soup.find('div', {'id': 'references'}).get_text()
        referred_by_nums = re.findall('\d+', referred_by)
    
    referred_by_nums = list(dict.fromkeys(referred_by_nums))
    print(f'{atel_num}: {referred_by_nums}')
    
    # Extracts referenced ATel numbers
    referenced_nums = []
    element = soup.find('div', {'id': 'telegram'})
    links = element.find_all('a', href=True)
    string = 'https://www.astronomerstelegram.org/?read='

    for link in links:
        if((link['href'].find(string) != -1) and (link.get_text() != 'Previous') and (link.get_text() != 'Next')):
            num = re.search('\d+', link['href'])
            if(num.group() not in referred_by_nums):
                referenced_nums.append(num.group())

    referenced_nums = list(dict.fromkeys(referenced_nums))
    print(f'{atel_num}: {referenced_nums}')

    print()

session.close()