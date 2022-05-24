import ssl
import time
import queue
import threading
from random import randint, choice
from urllib.parse import urlparse
from http import cookiejar

import requests
from pystyle import Colorate, Colors, Write, Add, Center

from Data.UserAgent import UserAgent
from Data.Lists import DeviceTypes, Platforms, Channel, ApiDomain
from utils import *
from Data.banner import logo

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

requests.packages.urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
r                                 = requests.Session()
countQueue                        = queue.Queue()
sentRequests                      = 0
completed                         = False

r.cookies.set_policy(BlockCookies())

def Banner():
    clear_console()
    Banner1 = r"""
    ╔╦╗  ╦  ╦╔═  ╔═╗  ╦ ╦  ╔═╗  ╦═╗  ╔═╗
     ║   ║  ╠╩╗  ╚═╗  ╠═╣  ╠═╣  ╠╦╝  ║╣ 
     ╩   ╩  ╩ ╩  ╚═╝  ╩ ╩  ╩ ╩  ╩╚═  ╚═╝
            discord.gg/devcenter
"""

    Banner2 = logo

    print(Center.XCenter(Colorate.Vertical(Colors.cyan_to_green, Add.Add(Banner2, Banner1, center=True), 2)))

def sendView():
    proxy       = {f'{proxyType}': f'{proxyType}://{choice(proxyList)}'}
    platform    = choice(Platforms)
    osVersion   = randint(1, 12)
    DeviceType  = choice(DeviceTypes)
    headers     = {
                        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "user-agent": choice(UserAgent)
                    }
    appName     = choice(["tiktok_web", "musically_go"])
    Device_ID   = randint(1000000000000000000, 9999999999999999999)
    apiDomain   = choice(ApiDomain)
    channelLol  = choice(Channel)
    URI         = f"https://{apiDomain}/aweme/v1/aweme/stats/?channel={channelLol}&device_type={DeviceType}&device_id={Device_ID}&os_version={osVersion}&version_code=220400&app_name={appName}&device_platform={platform}&aid=1988"
    data        = f"item_id={itemID}&play_delta=1"

    try:
        req = r.post(URI, headers=headers, data=data, proxies=proxy, timeout=5, verify=False)
        return True
    except:
        return False

def sendShare():
    platform    = choice(Platforms)
    osVersion   = randint(1, 12)
    DeviceType  = choice(DeviceTypes)
    headers     = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": choice(UserAgent)
    }
    appName     = choice(["tiktok_web", "musically_go"])
    Device_ID   = randint(1000000000000000000, 9999999999999999999)
    apiDomain   = choice(ApiDomain)
    channelLol  = choice(Channel)
    URI         = f"https://{apiDomain}/aweme/v1/aweme/stats/?channel={channelLol}&device_type={DeviceType}&device_id={Device_ID}&os_version={osVersion}&version_code=220400&app_name={appName}&device_platform={platform}&aid=1988"
    data        = f"item_id={itemID}&share_delta=1"

    try:
        req = r.post(URI, headers=headers, data=data, verify=False)
        return True
    except:
        return False

def clearURL(link):
    parsedURL = urlparse(link)
    host = parsedURL.hostname.lower()
    if "vm.tiktok.com" == host or "vt.tiktok.com" == host:
        UrlParsed = urlparse(r.head(link, verify=False, allow_redirects=True, timeout=5).url)
        return UrlParsed.path.split("/")[3]
    else:
        UrlParsed = urlparse(link)
        return UrlParsed.path.split("/")[3]

def proccessThread(sendProccess):
    while not completed:
        if sendProccess():
            countQueue.put(1)

def countThread():
    global sentRequests, completed
    while True:
        countQueue.get()
        sentRequests += 1
        if amount > 0:
            if sentRequests >= amount:
                completed = True

def progressThread():
    global sentRequests, elapsedReq
    while True:
        start = time.time()
        startReq = sentRequests
        time.sleep(1)
        end = time.time()
        endReq = sentRequests

        elapsed = end - start
        elapsedReq = endReq - startReq
        
        set_console_title(f"Thread :{str(threading.active_count() - 1)} / Try :{sentRequests}")
        Write.Print(f"{sentRequests} sent requests! {elapsedReq} requests/second.", Colors.cyan_to_green, interval=0.0001, end="\r")


if __name__ == "__main__":
    clear_console()
    set_console_title(f"TikTokMassBotting Menu")
    Banner()
    sendType     = 1
    urls=[]
    with open('urls.txt','r',encoding='utf8') as f:
        urls=f.readlines()
    for VideoURI in urls:
        amount       = 200
        nThreads     = 5
        itemID       = clearURL(VideoURI)

        for proxyType in ['http','socks4','socks5']:

            proxyList = read_proxies_file()
            clear_console()
            set_console_title(f"TikTokMassBotting Running")
            Banner()

            print(Colorate.Horizontal(Colors.red_to_white, f"\n    Hits are not counted"))
            print(Colorate.Horizontal(Colors.red_to_white, f"    Bot started! Check your video stats in 5 minutes !"))

            if sendType == 0:
                sendProcess = sendView
            elif sendType == 1:
                sendProcess = sendShare
            else:
                print(f"Error {sendType}")

            threading.Thread(target=countThread).start()
            threading.Thread(target=progressThread).start()

            for n in range(nThreads):
                threading.Thread(target=proccessThread, args=(sendProcess,)).start()