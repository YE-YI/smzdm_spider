import itchat
import requests
import sys

from apscheduler.schedulers.blocking import BlockingScheduler

username = ****
password = ****
class smzdmSpider:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {
            'Host': 'zhiyou.smzdm.com',
            # 签到验证头必要
            'Referer':'http://www.smzdm.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'
            }
        self.session = requests.Session()

    # 登录
    def login(self):
        formData = {
            'is_third': '0',
            'rememberme': '1',
            'redirect_to': 'http://www.smzdm.com/',
            'Host': 'zhiyou.smzdm.com',
        }

        formData['username'] = self.username
        formData['password'] = self.password
        loginURL = 'https://zhiyou.smzdm.com/user/login/ajax_check'
        try:
            req = self.session.post(loginURL, data=formData, headers=self.headers)
            return req.json()['error_code']
        except Exception as e:
            print('login error', e)
            sys.exit(1)

    # 自动签到
    def checkIn(self):
        signURL = 'http://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        print(self.session.cookies)
        checkinREQ = self.session.get(signURL, headers=self.headers)
        print(checkinREQ.json())
        return checkinREQ.json()['data']


    def start(self):
        loginData = self.login()
        if loginData == 0:
            print("登录成功")
            print("开始自动签到中")
        else:
            print("登录失败退出")
            sys.exit(1)
        try:
            checkinData = self.checkIn()
            if checkinData:
                print('签到成功')
                print('本次签到增加积分:', checkinData['add_point'])
                print('连续签到次数:', checkinData['checkin_num'])
                print('总积分:', checkinData['point'])
            else:
                print('签到失败,请检查用户名和密码后重新运行.')
        except Exception as e:
            print("签到失败",e)

# if __name__ == "__main__":
#     smzmdLogin = smzdmSpider(username, password)
#     smzmdLogin.start()

def my_job():
    smzmdLogin = smzdmSpider(username, password)
    smzmdLogin.start()


SIGN_IN_MP_DICT = {
    u'招商银行信用卡': u'周五流量', }

# 微信登陆
def wx_login():
    itchat.auto_login(True)


def wx_job():
    for mpName in SIGN_IN_MP_DICT.keys():
        mpList = itchat.search_mps(name=mpName)
        if len(mpList) != 1:
            print(u'没有检测到公众号“%s”，请检查名称')
            break
    for k, v in SIGN_IN_MP_DICT.items():
        itchat.send(msg=v, toUserName=itchat.search_mps(name=k)[0]['UserName'])
        print("签到消息发送成功")

sched = BlockingScheduler()
print('脚本开始')
sched.add_job(my_job,'interval', hours=24, misfire_grace_time=50)
wx_login()
print('招商银行每周五流量开始')
# 每周五10点16点开始前2分钟每20秒调用一次
sched.add_job(wx_job, 'cron', day_of_week='fri', hour='10,16', second='*/20', minute='0,1', misfire_grace_time=10)
sched.start()

