# Copy paste on top of importer.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Copy paste inside download_report
try:
    url = f'https://www.astronomerstelegram.org/?read={atel_num}'
        
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    browser = webdriver.Chrome('2021-10-tracking-astronomical-events/backend/controller/importer/chromedriver.exe', options=chrome_options)
    browser.get(url)

    html = browser.page_source

    return html
except ConnectionError as err:
    raise NetworkError(f'Network failure encountered: {str(err)}')
except HTTPError as err:
    raise NetworkError(f'Network failure encountered: {str(err)}')
except TimeoutError as err:
    raise DownloadFailError(f'Couldn\'t download HTML: {str(err)}')
finally:
    browser.quit()