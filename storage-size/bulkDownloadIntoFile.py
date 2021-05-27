from bs4 import BeautifulSoup
import sys
from requests_html import HTMLSession
from os import path



# Opens HTTP connection
session = HTMLSession()

for i in range(14, 15):
    # Create URL
    url = 'https://www.astronomerstelegram.org/?read=' + str(i)

    # Download HTML
    request = session.get(url)
    request.html.render(timeout=20)

    terminal = sys.stdout

    htmlText = BeautifulSoup(request.html.raw_html,'html.parser')

    filePath = path.relpath('storage-size/output/atel'+str(i)+'.txt')
    with open(filePath, 'w') as f:
        sys.stdout = f 
        print(htmlText)
        sys.stdout = terminal

session.close()