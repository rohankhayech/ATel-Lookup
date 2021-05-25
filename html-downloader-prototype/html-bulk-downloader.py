from requests_html import HTMLSession

import time

# Opens HTTP connection
session = HTMLSession()

# Bulk download start time
start = time.perf_counter()
# Current download start time
current = start

# Downloads 10 HTMLs
for i in range(1, 11):
    # Creates URL
    url = 'https://www.astronomerstelegram.org/?read=' + str(i)

    # Downloads HTML
    request = session.get(url)
    request.html.render(timeout=20)

    # Calculates download total time
    now = time.perf_counter()
    download_time = round(now - current, 2)
    current = now

    print(str(i) + ': ' + str(download_time) + ' seconds to download')

# Closes HTTP connection
session.close()

# Calculates bulk download total time
total_time = round(time.perf_counter() - start, 2)
print('\nTotal Download Time: ' + str(total_time) + ' seconds')
