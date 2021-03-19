from requests import get as req_get
from requests import post as req_post
from requests.exceptions import ConnectionError as ConnectException
from os import access as file_exists
from os import F_OK as file_exists_param
from bs4 import BeautifulSoup as NewBS
from colorama import init as colorama_init
from colorama import Back as back
from colorama import Fore as fore
from colorama import Style as style
from sys import exit as exit_
from time import sleep as time_sleep


colorama_init(autoreset=True)
is_installed = file_exists('config.txt', file_exists_param)
url = 'https://steamunlocked.net/among-us-free-download/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.190 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'accept': '*/*'
}


print('''
0000000 00   00 0000000 00    0 0000000     0     0 0000000
0     0 0 0 0 0 0     0 0 0   0 0           0     0 0
0000000 0  0  0 0     0 0  0  0 0   000     0     0 0000000
0     0 0     0 0     0 0   0 0 0     0     0     0       0
0     0 0     0 0000000 0    00 0000000      000000 0000000
'''[1:].replace('0', f'{fore.BLACK}{back.GREEN} {style.RESET_ALL}'), end='')


def get_html(link_url, params=None):
    return req_get(link_url, headers=headers, params=params)


def new_soup(html):
    soup = NewBS(html, 'html.parser')
    return soup


content = None

try:
    content = get_html(url).content
except ConnectException:
    print('No Internet Connection!')
    exit_(1)


def fast_read(filename):
    temp_f = open(filename, 'r')
    read_ = temp_f.read()
    temp_f.close()
    return read_


def fast_write(file_content, filename):
    temp_f = open(filename, 'w')
    temp_f.write(file_content)
    temp_f.close()


def upload_haven(link_to_download):
    file_storage = new_soup(get_html(link_to_download).content)
    form = file_storage.find_all('form', method='POST')[0]
    form_all_inputs = form.find_all('input')
    all_inputs = {
        '_token': form_all_inputs[0].get('value').strip(),
        'key': form_all_inputs[1].get('value').strip(),
        'time': form_all_inputs[2].get('value').strip(),
        'hash': form_all_inputs[2].get('value').strip()
    }
    time_sleep(6)
    result_form = req_post(link_to_download, headers=headers, data=all_inputs, params=all_inputs, timeout=2.50)
    fast_write(result_form.text, 'test.html')


def update_game():
    print(f'Downloading {steam_unlocked_check_title}...')
    link_to_download = steam_unlocked.find_all('a', class_='btn-download')[0].get('href').strip()
    print(f'Downloading from {link_to_download}...')
    upload_haven(link_to_download)
    fast_write(steam_unlocked_check_title, 'config.txt')


need_upgrade = False
steam_unlocked = new_soup(content)
steam_unlocked_check_title = steam_unlocked.find_all('div', class_='blog-content-title')[0].get_text(strip=True)


if is_installed:
    config = fast_read('config.txt').split('\n')
    if not steam_unlocked_check_title == config[0].strip():
        need_upgrade = True
else:
    need_upgrade = True

if need_upgrade:
    norm_title = steam_unlocked_check_title[25:-15]
    print(f'New Update! {norm_title}!')
    update_game()
