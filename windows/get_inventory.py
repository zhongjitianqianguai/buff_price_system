import urllib.request

import fake_useragent

ua = fake_useragent.UserAgent()
headers = {
    'User-Agent': str(ua.random),
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Referer': 'https://steamcommunity.com/',
}
url = 'https://gwapi.pwesports.cn/appdecoration/steamcn/csgo/decoration/getSteamInventory?steamId=76561198307802394'
no_proxy_handler = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(no_proxy_handler)
req = urllib.request.Request(url, headers=headers)
response = opener.open(req, timeout=15)
inventory = response.read().decode('utf-8')
print(inventory)
