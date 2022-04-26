import requests
from bs4 import BeautifulSoup
import ssl


URL = 'https://mignews.com/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0', 'accept': '*/*'}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


r = get_html(URL)
soup = BeautifulSoup(r.text, 'html.parser')
content = soup.findAll('div', class_='text-color-dark')
links_list = []
for item in content:
    #links = item.find('a').get('href')
    links = 'https://mignews.com'+item.find('a').get('href')
    links_list.append(links)
print(links_list)
box = []
for i in links_list:
    next = get_html(i)
    soup2 = BeautifulSoup(next.text, 'html.parser')
    title = soup2.find('div', class_='post-content post-article').find('h2', class_='font-weight-semibold text-5 line-height-6 my-1').text.strip()
    text = soup2.find('div', class_='post-content post-article').find('p').text.replace('\n', '').replace('\r', '').replace('\xa0', '')
    try:
        photo = 'https://mignews.com'+soup2.find('img', class_='img-fluid img-thumbnail img-thumbnail-no-borders rounded-0')['src']
    except:
        photo = 'None'
    box.append(
        {'title': title, 'content': text, 'photo': photo, 'category': {'title': 'Parser', 'id': 5}}
    )


res = ''
for item in box:
    print(item)
    res = requests.post('http://127.0.0.1:8000/api/news/', json=item)
    print(res.status_code)
    if res.status_code != 200:
        print(res.text)
        break









