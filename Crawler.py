import base64
from PIL import Image
import matplotlib.pyplot as plt
import json
import requests
import pandas as pd
import numpy as np
import multiprocessing
from threading import Thread
import time


def login(mobile_Phone_Number):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    }
    url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
    # 登录的网址。
    data = {'captcha_hash': '',
            'captcha_value': '',
            'mobile': mobile_Phone_Number,
            'scf': 'ms'
            }
    # 登录的参数。
    login = session.post(url, headers=headers, data=data)
    code = login.status_code
    if code == 200:  # 前三次登录没有图片验证过程
        token = login.json()['validate_token']
        print('成功发送,返回无图片验证码')
        url = 'https://h5.ele.me/restapi/eus/login/login_by_mobile'
        data2 = {
            'mobile': mobile_Phone_Number,
            'scf': 'ms',
            'validate_code': input('输入手机验证码：'),
            'validate_token': token
        }
        verify = session.post(url, headers=headers, data=data2)
        return verify.json()['user_id']
    elif code == 400:  # 登录超过3次，网站会要求图片验证
        print('有图片验证码')
        url = ' https://h5.ele.me/restapi/eus/v3/captchas'
        data2 = {'captcha_str': mobile_Phone_Number}
        # 提取验证码。
        cap = session.post(url, headers=headers, data=data2)
        code = cap.status_code
        strCap = cap.json()['captcha_image'].replace('data:image/jpeg;base64,', '')
        hash1 = cap.json()['captcha_hash']
        # 验证码字符串转图形文件保存到本地
        x = base64.b64decode(strCap)
        file = open('captcha.jpg', "wb")
        file.write(x)
        file.close()
        im = Image.open('captcha.jpg')
        im.show()  # 展示验证码图形
        captcha_value = input('输入验证码:')
        # 将图片验证码作为参数post到饿了吗服务器登录
        url = ' https://h5.ele.me/restapi/eus/login/mobile_send_code'
        data = {'captcha_hash': hash1,
                'captcha_value': captcha_value,
                'mobile': mobile_Phone_Number,
                'scf': 'ms'
                }
        # 将验证码发送到服务器。
        login = session.post(url, headers=headers, data=data)
        token = login.json()['validate_token']
        url = 'https://h5.ele.me/restapi/eus/login/login_by_mobile'

        data2 = {
            'mobile': mobile_Phone_Number,
            'scf': 'ms',
            'validate_code': input('输入手机验证码：'),
            'validate_token': token
        }
        verify = session.post(url, headers=headers, data=data2)  # 验证手机验证码
        return verify.json()['user_id']


def get_restauant(offset, longitude, latitude, headers):
    url = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude=' + str(latitude) + '&longitude=' + str(
        longitude) + '&keyword=&offset=' + str(
        offset) + '&limit=8&extras[]=activities&extras[]=tags&terminal=h5&brand_ids[]=&restaurant_category_ids[]=11'
    r = requests.get(url, headers=headers)
    result = json.loads(r.text)
    try:
        restaurant_list = result['items']
        return restaurant_list
    except:
        pass
        # time.sleep(5)


def get_total(longitude, latitude, headers):
    url = 'https://h5.ele.me/restapi/shopping/v2/restaurant/category?latitude=' + str(
        latitude) + '&longitude=' + str(
        longitude)
    r = requests.get(url, headers=headers)
    result = json.loads(r.text)
    for dic in result:
        category_name = dic.get("name")
        if category_name == "甜品饮品":
            return dic.get('count')
    return 0


def get_restaurant_name(id, user_id):
    url = 'https://h5.ele.me/restapi/booking/v1/cart_client'
    data = {"sub_channel": "", "business_type": 0, "geohash": "ws0eex8rp4u5", "user_id": user_id, "add_on_type": 0,
            "restaurant_id": id, "come_from": "mobile", "additional_actions": [71],
            "entities": [[]], "entities_with_ingredient": [[]], "operating_sku_ids": [], "tying_sku_entities": [[]],
            "packages": [[]]}
    r = requests.post(url, data=data)
    result = json.loads(r.text)
    # restaurant_name_list.append(result['cart']['restaurant']['address'])
    return result['cart']['restaurant']['address']


def get_result(longitude, latitude, user_id,total):
    total_list = []
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                             'like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36'
               }
    total_count = get_total(longitude, latitude, headers)
    if total_count == 0:
        return
    offset = 0
    while offset < total_count:
        restaurant_list = get_restauant(offset, latitude=latitude, longitude=longitude, headers=headers)
        # the_list = get_restauant(offset, latitude=latitude, longitude=longitude, headers=headers)
        try:
            for restaurant in restaurant_list:
                d = ['', '', '', '', '', '', '']
                d[0] = restaurant['restaurant']['name']
                d[1] = restaurant['restaurant']['flavors'][0]['name']
                d[2] = restaurant['restaurant']['id']
                d[3] = get_restaurant_name(d[2], user_id)
                d[4] = json.loads(restaurant['restaurant']['business_info'])['recent_order_num_display']
                d[5] = restaurant['restaurant']['longitude']
                d[6] = restaurant['restaurant']['latitude']
                d.remove(d[2])
                total_list.append(d)
            offset += 8
        except:
            break
    name = ['店铺名字', '类别', '地址', '月销售', '经度', '纬度']
    temp = pd.DataFrame(columns=name, data=total_list)
    list.append(temp)


if __name__ == '__main__':
    mobile_Phone_Number = input("请输入你的手机号:")
    user_id = login(mobile_Phone_Number)
    list = []
    # get_result(113.351075,23.160833)
    longitude_list = np.arange(112.758106, 115.420483, 0.018).tolist()
    latitude_list = np.linspace(22.205805, 23.963091, 100).tolist()
    name = ['店铺名字', '类别', '地址', '月销售', '经度', '纬度']
    total = pd.DataFrame(columns=name)
    for i in range(len(longitude_list)):
        for j in range(len(latitude_list)):
            print(i, j)
            # multiprocessing.Process(target=get_result(longitude_list[i], latitude_list[j], user_id=user_id,total=total)).start()
            try:
                multiprocessing.Process(target=get_result(longitude_list[i], latitude_list[j], user_id=user_id,total=total)).start()
            except:
                time.sleep(3)
                continue
            try:
                frames = [total, list[0]]
                total = pd.concat(frames)
                total = total.drop_duplicates()
                list.remove(list[0])
            except:
                pass

    total.to_csv('data.csv',encoding='utf-8')