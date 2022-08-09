import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time


start_time = time.time()


def get_links():
    URL = 'https://mignews.com/'
    HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
               'accept': '*/*'}
    r = requests.get(url=URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.findAll('div', class_='text-color-dark')
    links_list = []
    for item in content:
        links = 'https://mignews.com'+item.find('a').get('href')
        links_list.append(links)
    return links_list


async def parse_each_link(session, link):
    box = []
    response = await session.get(url=link)
    soup2 = BeautifulSoup(await response.text(), 'html.parser')
    title = soup2.find('div', class_='post-content post-article').find('h2', class_='font-weight-semibold text-5 line-height-6 my-1').text.strip()
    text = soup2.find('div', class_='post-content post-article').find('p').text.replace('\n', '').replace('\r', '').replace('\xa0', '')
    try:
        photo = 'https://mignews.com'+soup2.find('img', class_='img-fluid img-thumbnail img-thumbnail-no-borders rounded-0')['src']
    except:
        photo = 'None'
    box.append(
        {'title': title, 'content': text, 'photo': photo, 'category': {'title': 'Parser', 'id': 5}}
    )
    return box


async def main(get_links):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for link in get_links:
            tasks.append(asyncio.create_task(parse_each_link(session, link)))
        results = await asyncio.gather(*tasks)
        for i in results:
            i = i[0]
            print(i)
            res = requests.post('http://127.0.0.1:8000/api/news/', json=i)
            print(res.status_code)
            if res.status_code != 200:
                print(res.text)
                break


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main(get_links()))

    end_time = time.time() - start_time
    print(f"Spend time: {end_time}")