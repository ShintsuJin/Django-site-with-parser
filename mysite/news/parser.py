import requests
from bs4 import BeautifulSoup
import ssl
import time
import datetime
import os.path


start_time = time.time()
URL = 'https://mignews.com/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0', 'accept': '*/*'}


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_links(URL):
    r = get_html(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.findAll('div', class_='text-color-dark')
    links_list = []
    for item in content:
        #links = item.find('a').get('href')
        links = 'https://mignews.com'+item.find('a').get('href')
        links_list.append(links)
    return links_list


box = []
box_for_images = []
for i in get_links(URL):
    next = get_html(i)
    soup2 = BeautifulSoup(next.text, 'html.parser')
    title = soup2.find('div', class_='post-content post-article').find('h2', class_='font-weight-semibold text-5 line-height-6 my-1').text.strip()
    text = soup2.find('div', class_='post-content post-article').find('p').text.replace('\n', '').replace('\r', '').replace('\xa0', '')
    try:
        photo_for_upload = 'https://mignews.com'+soup2.find('img', class_='img-fluid img-thumbnail img-thumbnail-no-borders rounded-0')['src']
        photo = soup2.find('img', class_='img-fluid img-thumbnail img-thumbnail-no-borders rounded-0')['src'].split('/')[-1][0:-4] + '.jpg'
        image = f'photos/{year}/{month}/{day}/{photo}'
    except:
        photo = 'None'
        image = photo
        photo_for_upload = image
    box.append(
        {'title': title, 'content': text, 'photo': image, 'category': {'title': 'Parser', 'id': 5}}
    )
    box_for_images.append(photo_for_upload)


dirname = f'/home/nick/django3/mysite/media/photos/{year}/{month}/{day}'
if not os.path.exists(dirname):
    os.makedirs(dirname)


for j in box_for_images:
    if j == 'None':
        continue
    else:
        image_name = j.split('/')[-1][0:-4]
        file_path = f'/home/nick/django3/mysite/media/photos/{year}/{month}/{day}/{image_name}.jpg'
        if os.path.exists(file_path):
            continue
        else:
            p = requests.get(j)
            out = open(f'/home/nick/django3/mysite/media/photos/{year}/{month}/{day}/{image_name}.jpg', "wb")
            out.write(p.content)
            out.close()


res = ''
for item in box:
    print(item)
    res = requests.post('http://127.0.0.1:8000/api/news/', json=item)
    print(res.status_code)
    if res.status_code != 200:
        print(res.text)
        break


end_time = time.time() - start_time
print(f"Spend time: {end_time}")







