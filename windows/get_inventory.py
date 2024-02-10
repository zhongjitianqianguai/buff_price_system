import gzip
import json
import time
import urllib.request
import urllib.parse
from io import BytesIO

import fake_useragent
import requests
# ua = fake_useragent.UserAgent()
# headers = {
#     'User-Agent': str(ua.random),
#     'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#     'Referer': 'https://steamcommunity.com/',
# }
# url = 'https://gwapi.pwesports.cn/appdecoration/steamcn/csgo/decoration/getSteamInventory?steamId=76561198307802394'
# no_proxy_handler = urllib.request.ProxyHandler({})
# opener = urllib.request.build_opener(no_proxy_handler)
# req = urllib.request.Request(url, headers=headers)
# response = opener.open(req, timeout=15)
# inventory = response.read().decode('utf-8')
# print(inventory)
ua = fake_useragent.UserAgent()
headers = {
    'User-Agent': str(ua.random),
    'Host': 'www.csgoob.com',
    'Referer': 'https://steamcommunity.com/',
    'Cookie': 'cf_clearance=qlN6vFeTz5aj0homh522.DuaRr3Oyaa.u7GV5n1HgGg-1698283360-0-1-df376300.5716cdd3.88363ce0-0.1'
              '.1698283360',
    'Content-Length': '179',
    'Sec-Ch-Ua': '(Not(A:Brand";v="8", "Chromium";v="99',
    'Sec-Ch-Ua-Mobile': '?0',
    'Auth': '1b8443e6265a25d76176af86cc21e810',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Timestamp': str(time.time()).split('.')[0],
    'Sec-Ch-Ua-Platform': "Windows",
    'Origin': 'https://www.csgoob.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
url = 'https://www.csgoob.com/api/v1/goods/chart'
data = {"goods": [{"goodsId": "673415", "platform": 2}, {"goodsId": "1128403846100041728", "platform": 3},
                  {"goodsId": "928006", "platform": 0}, {"goodsId": "103739", "platform": 1}], "timeRange": "WEEK"}
req = requests.post(url,data=json.dumps(data),headers=headers)  # 发post请求,以json字符串参数格式
print(req.text)



