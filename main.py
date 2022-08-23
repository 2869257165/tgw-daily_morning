from datetime import date, datetime
from email.utils import localtime
import math
import re
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
# start_date = os.environ['START_DATE']
# city = os.environ['CITY']
# birthday = os.environ['BIRTHDAY']

# app_id = os.environ["APP_ID"]
# app_secret = os.environ["APP_SECRET"]

# user_id = os.environ["USER_ID"]
# template_id = os.environ["TEMPLATE_ID"]

city="上海市"
birthday="11-11"
start_date="2000-11-11"
app_id="wxcd88378bc2d221a1"
app_secret="c4d429fcb55f86a64267f4316f34aeb8"

user_id="oUq7H5g3y_9RiIa2i8-LTQXl_phE"
monring_template_id="DE7vj8nzeLYJ-wtqbs4asZOj9X5osjRu-xkr5hjIjoo"
lucky_template_id="ENLA3JB2KaxbtTUvVgf-alMCfuNb0R-FJA-7mcD36OI"
tianxing_key="10bfe3c26458704bf6cdd5c30a01ff71"

def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)

#获取距离生日的天数
def get_birthday():
  #获取今年的生日日期
  birthday_year=date.today().year        
  birthday_month = int(birthday.split("-")[0])
  birthday_day = int(birthday.split("-")[1])
  next=date(birthday_year,birthday_month,birthday_day)
  if next < date.today():
    #生日已经过了，以下一年的生日为准
    next=next.replace(year=next.year+1);
  return (next-date.today()).days
  

#获取天气
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])


def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

#获取天气等信息
def tip():
  url="http://api.tianapi.com/tianqi/index"
  params={"key": tianxing_key,"city":city}
  headers = {'Content-type':'application/x-www-form-urlencoded'}
  res=requests.get(url=url,params=params,headers=headers).json()
  weather=res["newslist"][0]["weather"]
  lowTem=res["newslist"][0]["lowest"]
  highTem=res["newslist"][0]["highest"]
  pop=res["newslist"][0]["pop"]
  tips=res["newslist"][0]["tips"]
  return weather,lowTem,highTem,pop,tips

#星座运势
def lucky():
    url="http://api.tianapi.com/star/index"
    params={'key':tianxing_key,'astro':"virgo"}
    headers = {'Content-type':'application/x-www-form-urlencoded'}
    res=requests.get(url=url,params=params,headers=headers).json()
    data = "综合指数: "+str(res["newslist"][0]["content"])+"\n爱情指数: 0(没有我就不能有哈!嘿嘿！)"+"\n工作指数: "+str(res["newslist"][2]["content"])+"\n今日概述："+str(res["newslist"][8]["content"])
    return data;    
  
#健康小提示API
def health():
  url="http://api.tianapi.com/healthtip/index"
  params={'key':tianxing_key}
  headers = {'Content-type':'application/x-www-form-urlencoded'}
  res=requests.get(url=url,params=params,headers=headers).json()
  headers = {'Content-type':'application/x-www-form-urlencoded'}
  health_tip=res["newslist"][0]["content"]
  return health_tip
    
#彩虹屁
def caihongpi():
  url="http://api.tianapi.com/caihongpi/index"
  headers={'Content-type':'application/x-www-form-urlencoded'}
  params={'key':tianxing_key}
  res=requests.get(url=url,params=params,headers=headers).json()
  data=res["newslist"][0]["content"]
  if("XXX" in data):
   data.replace("XXX","格格")
  return data


def get_access_token():
  url = "https://api.weixin.qq.com/cgi-bin/token"
  params={'grant_type':"client_credential",'appid':app_id,'secret':app_secret}
  res= requests.get(url,params=params).json()
  print(res)
  access_token=res["access_token"]
  print(access_token)
  return access_token

#推送早安信息
def send_monring_message( access_token, datevalue,weather, birthday_day, lowTem,highTem, pop, tips):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    data = {
        "touser": user_id,
        "template_id": monring_template_id,
        "url": "http://weixin.qq.com/download",
        "data": {
            "date": {
                "value": datevalue,
                "color": get_color()
            },
            "city": {
                "value": city,
                "color": get_color()
            },
            "birthday":{
              "value": birthday_day,
              "color":get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "min_temperature": {
                "value": lowTem,
                "color": get_color()
            },
            "max_temperature": {
                "value": highTem,
                "color": get_color()
            },
            "pop": {
                "value": pop,
                "color": get_color()
            },
            "tips": {
                "value": tips,
                "color": get_color()
             }
          }
    }
    print(data)
    response = requests.post(url, headers=headers, json=data).json()
    print(response)

#推送星座寄语信息
def send_lucky_message( access_token,pipi,lucky_data):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    data = {
        "touser": user_id,
        "template_id": lucky_template_id,
        "url": "http://weixin.qq.com/download",
        "data": {
            
            "lucky": {
                "value": lucky_data,
                "color": get_color()
             },
             "pipi":{
                "value": pipi,
                "color": get_color()
             }
          }
    }
    print(data)
    response = requests.post(url, headers=headers, json=data).json()
    print(response)


if __name__ == "__main__":
  #  client = WeChatClient(app_id, app_secret)
  #  wm = WeChatMessage(client)
  #  wea, temperature = get_weather()
  #  data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
  #  res = wm.send_template(user_id, template_id, data)

  #今天的日期yyyy-mm0-dd 星期x
  curdate=str(localtime().date())
  weakday = localtime().weekday()
  weak_list=["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"]
  datevalue=curdate+" "+weak_list[weakday]
  #获得天气等信息
  weather,lowTem,highTem,pop,tips = tip()
  #获取距离生日还有多少天
  birthday_day=get_birthday()
  #获得星座祝愿
  lucky_data = lucky()
  #获取健康小提醒
  health_tip=health()
  #彩虹屁
  pipi=caihongpi()

  #获取token
  token= get_access_token()
  print(token)
  #发送请求
  send_monring_message(access_token=token,datevalue=datevalue,weather=weather,birthday_day=birthday_day,lowTem=lowTem,highTem=highTem,pop=pop,tips=tips)
  send_lucky_message(access_token=token,pipi=pipi,lucky_data=lucky_data)
