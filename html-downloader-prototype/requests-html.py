from bs4 import BeautifulSoup
from requests_html import HTMLSession

session = HTMLSession()

request = session.get('https://www.astronomerstelegram.org/?read=14623')
request.html.render()

soup = BeautifulSoup(request.html.raw_html,'html.parser')
print(soup.find('h1', {'class': 'title'}).get_text())
