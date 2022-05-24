import os
import random
from time import sleep
from selenium import webdriver
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from utils import read_proxies_file
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Credit to Pycenter by billythegoat356
# Github: https://github.com/billythegoat356/pycenter/
# License: https://github.com/billythegoat356/pycenter/blob/main/LICENSE


# def center(var: str, space: int = None):  # From Pycenter
#     if not space:
#         space = (os.get_terminal_size().columns -
#                  len(var.splitlines()[int(len(var.splitlines())/2)])) / 2

#     return "\n".join((' ' * int(space)) + var for var in var.splitlines())


class Fore:
    YELLOW = '\033[93m'
    GREEN = '\033[32m'
    RED = '\033[91m'
    CYAN = '\033[36m'
    RESET = '\033[0m'


proxies = []


def banner():
    os.system(
        'cls && title [YT View Bot v2] - Made by Plasmonix' if os.name == "nt" else 'clear')
    text = '''                          
                     ▓██   ██▓▄▄▄█████▓    ██▒   █▓ ██▓▓█████  █     █░    ▄▄▄▄    ▒█████  ▄▄▄█████▓
                      ▒██  ██▒▓  ██▒ ▓▒   ▓██░   █▒▓██▒▓█   ▀ ▓█░ █ ░█░   ▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒
                       ▒██ ██░▒ ▓██░ ▒░    ▓██  █▒░▒██▒▒███   ▒█░ █ ░█    ▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░
                       ░ ▐██▓░░ ▓██▓ ░      ▒██ █░░░██░▒▓█  ▄ ░█░ █ ░█    ▒██░█▀  ▒██   ██░░ ▓██▓ ░ 
                       ░ ██▒▓░  ▒██▒ ░       ▒▀█░  ░██░░▒████▒░░██▒██▓    ░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░ 
                        ██▒▒▒   ▒ ░░         ░ ▐░  ░▓  ░░ ▒░ ░░ ▓░▒ ▒     ░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░   
                      ▓██ ░▒░     ░          ░ ░░   ▒ ░ ░ ░  ░  ▒ ░ ░     ▒░▒   ░   ░ ▒ ▒░     ░    
                      ▒ ▒ ░░    ░              ░░   ▒ ░   ░     ░   ░      ░    ░ ░ ░ ░ ▒    ░      
                      ░ ░                       ░   ░     ░  ░    ░        ░          ░ ░           
                      ░ ░                      ░                                ░                '''
    faded = ''
    cyan = 100
    for line in text.splitlines():
        faded += (f"\033[38;2;0;255;{cyan}m{line}\033[0m\n")
        if not cyan == 255:
            cyan += 15
            if cyan > 255:
                cyan = 255
    # print(center(faded))
    # print(
        # center(f'{Fore.YELLOW}\ngithub.com/Plasmonix Version 2.0{Fore.RESET}'))


def load_proxies():
    try:
        proxyfile = open(fp, "r+").readlines()
        for proxy in proxyfile:
            ip = proxy.split(":")[0]
            port = proxy.split(":")[1]
            proxies.append({
                'ip': ip.rstrip("\n"),
                'port': port.rstrip("\n")})
    except:
        print(f'[{Fore.RED}!{Fore.RESET}] {Fore.RED}File not found{Fore.RESET}')
        quit()


ua = UserAgent()


def scrape_proxies():
    try:
        proxies_req = Request('https://www.sslproxies.org/')
        proxies_req.add_header('User-Agent', ua.random)
        proxies_doc = urlopen(proxies_req).read().decode('utf8')
        soup = BeautifulSoup(proxies_doc, 'html.parser')
        proxies_table = soup.find(
            'table', attrs={'class': 'table table-striped table-bordered'})
        for row in proxies_table.tbody.find_all('tr'):
            proxies.append({
                'ip':   row.find_all('td')[0].string,
                'port': row.find_all('td')[1].string})
    except:
        print(
            f'[{Fore.RED}!{Fore.RESET}] {Fore.RED}Failed to scrape proxies{Fore.RESET}')
        quit()


def load_url(videoname,url,ua, sleeptime, proxy):
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' %
                         (proxy['ip'] + ':' + proxy['port']))
    options.add_argument('user-agent=%s' % ua.random)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    videoquery='+'.join(videoname.split(' '))
    searchurl='https://www.youtube.com/results?search_query='+videoquery
    driver.get(searchurl)
    sleep(20)
    driver.get(url)
    sleep(sleeptime)
    driver.quit()


if __name__ == "__main__":
    banner()
    try:
        items = []
        scrape_proxies()
        for proxyType in ['http','socks4','socks5']:

            proxyList = read_proxies_file()
            proxies.extend(proxyList)
        with open('urls.txt', 'r', encoding='utf8') as f:
            items = f.readlines()
        for item in items:

            views = 200
            minwatch = 60
            maxwatch = 180
            videoname=item.split(',')[-1]
            url=item.split(',')[0]

            for i in range(views):
                sleeptime = random.randint(minwatch, maxwatch)
                proxy = random.choice(proxies)
                load_url(videoname,url,ua, sleeptime, proxy)
    except ValueError:
        print(
            f'[{Fore.RED}!{Fore.RESET}] {Fore.RED}Value must be an integer{Fore.RESET}')
        quit()

#     os.system('cls')
#     banner()
#     for i in range(views):
#         sleeptime = random.randint(minwatch,maxwatch)
#         proxy = random.choice(proxies)
#         load_url(ua, sleeptime, proxy)
