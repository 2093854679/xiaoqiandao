import json

import requests


class xiaoqiandao:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "Referer": "https://servicewechat.com/wxee55405953922c86/622/page-frame.html",
        }
        self.access_token = input("请输入token:")

    def __call__(self):
        self.getlist()
        self.getcid()
        self.qiandao()

    # 获取打卡列表
    def getlist(self):
        url = f"https://api-xcx-qunsou.weiyoubot.cn/xcx/checkin/v3/list?type=5&page=1&count=10&access_token={self.access_token}&tag=0&keyword="
        page = requests.get(url, headers=self.headers)
        dict_page = page.json()

        datas = dict_page["data"]

        id = 0
        checkins = []
        for data in datas:
            title = data["title"]
            cid = data["cid"]
            owner = data["owner"]

            checkin = {"id": id, "title": title, "owner": owner, "cid": cid}
            checkins.append(checkin)
            print(checkin)

            id += 1

        id = input("请输入对应的id:")

        self.cid = checkins[int(id)]["cid"]

    # 获取打卡指定的位置信息
    def getcid(self):
        url = f"https://api-xcx-qunsou.weiyoubot.cn/xcx/checkin/v4/detail?cid={self.cid}&access_token={self.access_token}&tag=0&random_num=0.9361229083976608"
        page = requests.get(url, headers=self.headers)
        dict_page = page.json()

        print("\n检查必填项中")

        self.field_names = []
        fill_options = dict_page["data"]["fill_options"]
        for fill_option in fill_options:
            if fill_option["require"]:
                self.field_names.append(fill_option["field_name"])

        if not self.field_names:
            print("无必填项")
        else:
            print("必填项有:")
            for field_name in self.field_names:
                print(field_name)

        if "地理位置" in self.field_names:
            self.val = dict_page["data"]["locations"][0]["address"]
            self.lat = round(float(dict_page["data"]["locations"][0]["latitude"]), 5)
            self.lon = round(float(dict_page["data"]["locations"][0]["longitude"]), 5)

            print("\n将使用此地址签到:", self.val)

    def qiandao(self):
        url = "https://api-xcx-qunsou.weiyoubot.cn/xcx/checkin/v3/doit"

        if "地理位置" in self.field_names:
            data = {
                "cid": self.cid,
                "access_token": self.access_token,
                "fill_params": [
                    {"key": 6, "val": self.val, "lat": self.lat, "lon": self.lon}
                ],
            }
        else:
            data = {
                "cid": self.cid,
                "longitude": 0,
                "latitude": 0,
                "access_token": self.access_token,
            }

        print("\n开始签到")
        # data表单必须先处理成json数据后才能发送
        page = requests.post(url, headers=self.headers, data=json.dumps(data))

        if page.json()["msg"] == "ok":
            print("签到成功")

        print("\n服务器返回的信息:", page.text)


if __name__ == "__main__":
    xia = xiaoqiandao()
    xia()
