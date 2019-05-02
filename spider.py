import requests
import json
import os
import hashlib
from multiprocessing import Pool


def get_index(page_num):
    url = 'https://api.vc.bilibili.com/link_draw/v2/Photo/list?category=sifu&type=hot&page_num={}&page_size=20'.format(page_num)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code, 'from get_index')
    except requests.RequestException:
        print('RequestException')


def parse(dct):
    items = dct.get('data').get('items')
    for i in items:
        yield {
            'name': i.get('user').get('name'),
            'uid': i.get('user').get('uid'),
            'doc_id': i.get('item').get('doc_id'),
            'pictures': [i.get('img_src') for i in i.get('item').get('pictures')],
            'title': i.get('item').get('title')
        }


def get_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        print(response.status_code, 'from image')
    except requests.RequestException:
        print('RequestException from image')


def save_image(data):
    target_dir = '{}/{} {}'.replace('/', os.sep).format(data.get('name'), data.get('title'), data.get('doc_id')).replace(' ', '_')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        html_name = '{} {}.html'.format(data.get('title'), data.get('name')).replace(' ', '_')
        with open(target_dir + os.sep + html_name, 'a') as ff:
            for url in data.get('pictures'):
                content = get_image(url)
                if content:
                    image_name = hashlib.md5(content).hexdigest() + '.' + 'jpg'
                    path = target_dir + os.sep + image_name
                    if not os.path.exists(path):
                        with open(path, 'wb') as f:
                            f.write(content)
                        ff.write('<img src="{}" width="1000">'.format(image_name))


def isblocked(dct):
    name = dct.get('name').lower()
    title = dct.get('title').lower()
    for i in ['洛丽塔', 'lolita', '汉服', '古装', '妆', '女装', '山海经', '十音']:
        if i in name or i in title:
            return True
    return False


def main(page_num):
    html = get_index(page_num)
    if html:
        for data in parse(html):
            if isblocked(data):
                continue
            print(data.get('name') + '\t\t\t\t' + data.get('title'))
            save_image(data)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, list(range(0, 30)))
