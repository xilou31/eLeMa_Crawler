import json
import requests
import pandas as pd
import numpy as np
import time


def get_restauant(offset, header, longitude, latitude):
    url = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude=' + str(latitude) + '&longitude=' + str(
        longitude) + '&keyword=&offset=' + str(
        offset) + '&limit=8&extras[]=activities&extras[' \
                  ']=tags&terminal=h5&rank_id=222dafdcdd9a447e97375ce485f3e2ad&brand_ids[' \
                  ']=&restaurant_category_ids[]=-102 '
    r = requests.get(url, headers=header)
    result = json.loads(r.text)
    restaurant_list = result['items']
    total_list.append(restaurant_list)


def get_total(longitude, latitude):
    url = 'https://h5.ele.me/restapi/shopping/v2/restaurant/category?latitude=' + str(latitude) + '&longitude=' + str(
        longitude)
    r = requests.get(url)
    result = json.loads(r.text)
    for dic in result:
        category_name = dic.get("name")
        if category_name == "甜品饮品":
            return dic.get('count')
    return 0


def fil(old_string):
    new_string = []
    for c in old_string:
        if (c >= '0') & (c <= '9'):
            new_string.append(c)
        else:
            continue
    return new_string


def get_restaurant_name(id):
    url = 'https://h5.ele.me/restapi/booking/v1/cart_client'
    data = {"sub_channel": "", "business_type": 0, "geohash": "ws0eex8rp4u5", "user_id": 2014785793, "add_on_type": 0,
            "restaurant_id": id, "come_from": "mobile", "additional_actions": [71],
            "entities": [[]], "entities_with_ingredient": [[]], "operating_sku_ids": [], "tying_sku_entities": [[]],
            "packages": [[]]}
    r = requests.post(url, data=data)
    result = json.loads(r.text)
    return result['cart']['restaurant']['address']


def get_result(longitude, latitude):
    total_count = get_total(longitude, latitude)
    if total_count == 0:
        return
    offset = 0
    header = {
        'cookie': 'ubt_ssid=cmqbrw0dditxri4uohu24duie4xa8qnk_2019-09-23; '
                  'perf_ssid=ik1b57w1wnyac23029rjexj1rz3cjmou_2019-09-23; cna=5dWkFbfoOy8CAX1YGIrG6fe6; '
                  '_utrace=88d11b084d20ec888553b1da0026c8eb_2019-09-23; '
                  'ut_ubt_ssid=sx8kew8r4if9eq9225ozjm7dul6g7u42_2019-09-23; '
                  'track_id=1569251986|b2b4bf1e89411d9fe0e5cd50e46456141740833ac43b7a0b2a'
                  '|ce3ff3e71aa873a9460122dad833d050; USERID=2014785793; tzyy=c509115f45309f970d4abe0e479d95bb; '
                  'UTUSER=2014785793; SID=VNhX0gKnjW4iX8ECBJsXqGbd37oJbUOsN3sQ; '
                  'ZDS=1.0|1569850888|V5KQsKt9QZMSwPnoiP6GvgMpIR8qXPCQQBY1LlhzZ6lK0k4DrJtQf'
                  '/drvNRO59WiVkkVMD7tRMSVmObU8WYqRg==; '
                  'pizza73686f7070696e67=CPuz42fVoxnRVcVQ1x33fTWTZKSVMwc92D6xv0VaBXuu95-1uhZ3grUqOez8H1fS; '
                  'isg=BBcXOCu0BvxUtoJquw8jt-hrpothXOu-K4GzpmlEZuZNmDfacCh0DiWx-ngjcMM2; '
                  'l=cBMZyV2rqXNe1GMpBOCwnurza77tTIRAguPzaNbMi_5QL6L_c17Oktz0IFp6cjWdtqLp4tm2-g29-etk9RUGPSE9-vNV'
                  '.AWTZbmU5kQu1Fku17IVSIorMmTw; '
                  'isg=BIqKaA-O41cA2m_hpkhmbE2U23Asew7Vr3mEXhTDNV18xyyB_A5y5EZx01W-N4Zt'}
    while offset < total_count:
        get_restauant(offset, header, latitude=latitude, longitude=longitude)
        offset += 8
        print(offset)
    for the_list in total_list:
        for restaurant in the_list:
            d = ['', '', '', '', '', '', '']
            d[0] = restaurant['restaurant']['name']
            d[1] = restaurant['restaurant']['flavors'][0]['name']
            d[2] = restaurant['restaurant']['id']
            d[3] = get_restaurant_name(d[2])
            d[4] = "".join(fil(json.loads(restaurant['restaurant']['business_info'])['recent_order_num_display']))
            d[5] = restaurant['restaurant']['longitude']
            d[6] = restaurant['restaurant']['latitude']
            restaurant_list.append(d)


if __name__ == '__main__':
    total_list = []
    restaurant_list = []
    # get_result(113.351075,23.160833)
    longitude_list = np.linspace(113, 127).tolist()
    latitude_list = np.linspace(23, 46).tolist()
    for longitude in longitude_list:
        for latitude in latitude_list:
            get_result(longitude, latitude)
    name = ['店铺名字', '类别', 'id', '地址', '日销售', '经度', '纬度']
    result = pd.DataFrame(columns=name, data=restaurant_list)
    result.to_csv('data.csv', encoding='gbk')
