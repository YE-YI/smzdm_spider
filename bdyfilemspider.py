import requests
import sys

from apscheduler.schedulers.blocking import BlockingScheduler

username = '583260221'
password = '57871deab1979e4b3eaa551c8a3aa8f1'

class yunfilmSpider:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {
            # 签到验证头必要
            'Origin':'http://www.baiduyunfilm.com/',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            # 'Referer': "http://www.baiduyunfilm.com/forum.php?mod=viewthread&tid=28714&access_token=OsT7ZPnZ4o2e5uZuuTss4aMATiN4VizN&winzoom=1",
            'Host': 'www.baiduyunfilm.com'
        }
        self.session = requests.Session()

    # 登录
    def login(self):
        formData = {
            'fastloginfield': 'username',
            'quickforward': 'yes',
            'handlekey': '1s',
            'username': self.username,
            'password': self.password
        }
        loginURL = 'http://www.baiduyunfilm.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
        # loginURL += '&fastloginfield=username&username=%s&password=%s&quickforward=yes&handlekey=1s' % (self.username, self.password)
        try:
            rep = self.session.post(loginURL,data=formData, headers=self.headers)
            print(rep.status_code)
            return rep.status_code
        except Exception as e:
            print('login error', e)
            sys.exit(1)

    # 自动签到
    def checkIn(self):
        signURL = 'http://www.baiduyunfilm.com/plugin.php?id=dc_signin:sign&inajax=1'
        # signURL = 'http://www.baiduyunfilm.com/plugin.php?id=dc_signin:sign&inajax=1&signsubmit=yes&handlekey=signin&emotid=1&referer=http%3A%2F%2Fwww.baiduyunfilm.com%2Fplugin.php%3Fid%3Ddc_signin&content=%CE%D2%B0%AE%C1%D4%CA%D6%A3%AC%CE%D2%B0%AE%B5%E7%D3%B0%A3%A1'
        checkinREQ = self.session.get(signURL, headers=self.headers)
        print(checkinREQ.text)
        return checkinREQ.text


    def start(self):
        status_code = self.login()
        if status_code == 200:
            print("登录成功")
            print("开始自动签到中")
        else:
            print("登录失败退出")
            sys.exit(1)
        try:
            checkinData = self.checkIn()
        #     if checkinData:
        #         print('签到成功')
        #         print('本次签到增加积分:', checkinData['add_point'])
        #         print('连续签到次数:', checkinData['checkin_num'])
        #         print('总积分:', checkinData['point'])
        #     else:
        #         print('签到失败,请检查用户名和密码后重新运行.')
        except Exception as e:
            print("签到失败",e)

if __name__ == "__main__":
    filmLogin = yunfilmSpider(username, password)
    filmLogin.start()

# def my_job():
#     filmLogin = yunfilmSpider(username, password)
#     filmLogin.start()
#
# sched = BlockingScheduler()
# print('脚本开始')
# sched.add_job(my_job,'interval', hours=24, misfire_grace_time=50)
# sched.start()

