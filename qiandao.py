# 仅支持只需要定位信息的打卡
# 尚未完成

import json
import sys

import requests

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "Referer":
    "https://servicewechat.com/wxee55405953922c86/622/page-frame.html"
}

access_token = input("请输入token:")


# 获取打卡列表
def getlist():
    url = f"https://api-xcx-qunsou.weiyoubot.cn/xcx/checkin/v3/list?type=5&page=1&count=10&access_token={access_token}&tag=0&keyword="

    page = requests.get(url, headers=headers)

    dict_page = json.loads(page.content)

    try:
        datas = dict_page['data']
    except:
        print(str(dict_page))

        sys.exit()

    id = 0

    checkins = []

    for data in datas:
        title = data['title']

        cid = data['cid']

        owner = data['owner']

        checkin = {"id": id, "title": title, "owner": owner, "cid": cid}

        checkins.append(checkin)

        print(checkin)

        id += 1

    id = input("请输入对应的id:")

    cid = checkins[int(id)]["cid"]

    return cid


# 获取打卡指定的位置信息
def getcid(cid):
    url = f"https://api-xcx-qunsou.weiyoubot.cn/xcx/checkin/v4/detail?cid={cid}&access_token={access_token}&tag=0&random_num=0.9361229083976608"

    page = requests.get(url, headers=headers)

    dict_page = json.loads(page.content)

    val = dict_page['data']['locations'][0]['address']

    lat = round(float(dict_page['data']['locations'][0]['latitude']), 5)

    lon = round(float(dict_page['data']['locations'][0]['longitude']), 5)

    print('\n', val, "\n", lat, '\n', lon)

    return val, lat, lon


# 最后这一步虽然返回的状态码是200，但是签到打卡并没有成功
# 因此脚本没有完成
def qiandao(cid, val, lat, lon):
    url = "https://api-xcx-qunsou.weiyoubot.cn/xcx/checkin/v3/doit"

    data = {
        "cid": cid,
        "access_token": access_token,
        "fill_params": [{
            "key": 6,
            "val": val,
            "lat": lat,
            "lon": lon
        }]
    }

    page = requests.post(url, headers=headers, data=data)

    print(page.text)

    print(page.status_code)


cid = getlist()
val, lat, lon = getcid(cid)
qiandao(cid, val, lat, lon)
