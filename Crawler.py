import json
import requests
import pandas as pd
import numpy as np
import multiprocessing
from threading import Thread


def get_restauant(offset, longitude, latitude, headers):
    url = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude='+str(latitude)+'&longitude='+str(longitude)+'&keyword=&offset='+str(offset)+'&limit=8&extras[]=activities&extras[]=tags&terminal=h5&brand_ids[]=&restaurant_category_ids[]=11'
    r = requests.get(url, headers=headers)
    result = json.loads(r.text)
    try:
        restaurant_list = result['items']
        total_list.append(restaurant_list)
        print(result)
    except:
        print(result)
        return 0
        # time.sleep(5)


def get_total(longitude, latitude, headers):
    url = 'https://h5.ele.me/restapi/shopping/v2/restaurant/category?latitude=' + str(latitude) + '&longitude=' + str(
        longitude)
    r = requests.get(url, headers=headers)
    result = json.loads(r.text)
    for dic in result:
        category_name = dic.get("name")
        if category_name == "甜品饮品":
            return dic.get('count')
    return 0


def get_restaurant_name(id):
    url = 'https://h5.ele.me/restapi/booking/v1/cart_client'
    data = {"sub_channel": "", "business_type": 0, "geohash": "ws0eex8rp4u5", "user_id": 2014785793, "add_on_type": 0,
            "restaurant_id": id, "come_from": "mobile", "additional_actions": [71],
            "entities": [[]], "entities_with_ingredient": [[]], "operating_sku_ids": [], "tying_sku_entities": [[]],
            "packages": [[]]}
    r = requests.post(url, data=data)
    result = json.loads(r.text)
    restaurant_name_list.append(result['cart']['restaurant']['address'])
    # print(result['cart']['restaurant']['address'])


def get_result(longitude, latitude):
    headers = {'Accept': 'application/json, text/plain, */*',
               'Referer': 'https://h5.ele.me/msite/food/',
               'Sec-Fetch-Mode': 'cors',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Mobile Safari/537.36',
               'X-Shard': 'loc=113.357583,23.15765, loc=113.357583,23.15765',
               'x-uab': '120#bX1bSTNllAh2NLFV6CUsgzU//yOuoo6sE6jLCilKlqU2Pc8PnNg8NrSV1tQ/veqgBNmu8WnpUXH+xEH+NT4dOdid8TQKYO3yqNhR50befws/iVUrYRVFoZDawLrFxdNi8OfCbjcyknLFlAPs0l7Saz+bNFYvSi5/ybbS7UGPWWl/oYk6y/T9XJhy5IxYg6ikMx3xPrqwXJGqcp5pZOCcYoA8jPH9L7q6E5phfCPg8+JvnFBZ2zTQ6kl6X80NMK7bpI5ODxUZ7g5nVwaMfXeamZEFBh1/VmzFDXGem7vwQOsEssLHJCNkY3ci+ZNGm+K6Smt0BJ28xa321sW9Oj0VGL8+lyIJnykF1Y3LroXst4D6Rdj9byaciOLUnm/PCzS3EHOQ15CoZrazl+h76hTZG9o6Ayp1hh9Db7H+nHqVdWdP5D+B9Yj3fAVYOG5h73oE45BJp7PuuQgUAI5FHNQwDQGMRdOshwXvL0T5VSBMN6B7G6KvwnqWfzcX5NHpGcTdRdCcHzk8bhUtOtscrylqztHlTQpelwgZ2kxD3rWYSgXx6oCim/5nPeTDHtn894faPuwIPdvOJHO4xWaAG2plWnXwKmNCKwQHlOJ3xvSHgm/ppDdCCJNpzQfoxciLI03lO+MF3d+llaOZk9ZIAb82L6fa7sg30iegdQ9GVY4fSAa8aS2pof7fMKVsJ7MgOc8r6nrsBzTqDCL/HGYWJ/+lScywDeTGTv+n3a9i5AaIKnoWvLJD1/MNjJjU7bEGSxnYzJdXa9eoA4ue4CxeQ6npwXcFs1guMKx8iYw+oygF0aLFmb/Qz+Zhclou+ZaxY+VnXtisuRrY3uUDxzQQDAi47gHbJGD1HB93yTePtKJI9VLBPdmi4mxfYi83soX6gHHdWgfRxYmUyIT/gTnRgsY/htbavujsmXh0VPaVLDs7qyKNF3cshfGhhFqusr4ef/npZnhjTUEuyMBiYSJhkuMsyC73xaOvWA+lf7QjxtSGzarOKeR87cfckUhwAFGbSUOZoWMMRAoLP3tzFlijQvOz8deVFSEriqPpTZWU6N17WCM8jxfZlD86klFuq9PtMNQ95MkEHJR/jma06JitFuLxSC3bTF3CUJcV1l69m7f8XTCuUNcN0HvCepS/i5o8DPT1jJ7btkRfdtvBLWou/27+mGpo/CInk8iu5rzPAGeXrX436WeF18v8W3idO52B8qMgPiMMdXmf9tmD1tZb1C/DnzLHuzzs4ES1DGsaOQ1Tos/SLle0/LkimK2XmWtifwd/IqOprZwElDjnF9aP9hpPORGZcdsdemUTiiG5deQYeYuI5ZwlPG+27HL2u03a3S8zu6WiwhpVr56rB10kRa7o9CWVjtn/FzLdxD67dTgQxoSbngnzGei4cKj0SShqIu4OpCKf0ZUAgtpbNSt2PfkuNBsDJVIFnD4C+jqqwL9+DKfU7MjveBiLE2cSjEJLBs1Bv9dADG/wCnzONACB0Ak7Jui4KSGuoJ0kbH9cEMBWKmUCJ1x9++qFORVcunfnIRmNgWcfg1eN4zU6/G3q4SrDVpgWsKofLL+FXLrFMxHequD4/ZEqjYby1EBYrFI1GCD6J1+mUOUTXyNWHh7cCgMpw3cHGCVgG3evnHzPfLeg1ALeueAn0/YV6ADf2+EbQevUUHO3uve2LgogIAyrF2CB9dH39UcADtFFqpVBQ/lh++9NmDywDONBVkMWKtcfqOO8E6GaXFBWfUAPu8/ahAQrypB2RltsZmQEwukRaOMWu8HjdWr8glJZ+Shp0H/MJXhL0qwTird0vEwUYVcU17vbq+DetP7gCfncchC7wvqMBZyWexlnpeUKEGrY21c2TVxgwOIFXz66oC26cQ/z3xrmhuD5/n4mz00zt4o1ovdOyC6xpoERgToX3eJ1oDh8jh9kwaR36UZmNzikOw8DxdFnkzH05XXJK9W4Alp2eXiCCbobzep+FlpKd51o',
                'Cookie':'ubt_ssid=cmqbrw0dditxri4uohu24duie4xa8qnk_2019-09-23; cna=5dWkFbfoOy8CAX1YGIrG6fe6; '
                         '_utrace=88d11b084d20ec888553b1da0026c8eb_2019-09-23; '
                         'ut_ubt_ssid=sx8kew8r4if9eq9225ozjm7dul6g7u42_2019-09-23; '
                         'perf_ssid=nyu3zm5xqa8lc2nwabzqtmhv574lhxlo_2019-09-23; '
                         'track_id=1569251986|b2b4bf1e89411d9fe0e5cd50e46456141740833ac43b7a0b2a'
                         '|ce3ff3e71aa873a9460122dad833d050; tzyy=c509115f45309f970d4abe0e479d95bb; '
                         '_bl_uid=9skUz1bp4q5xeLob244kka6m5zpF; '
                         'ZDS=1.0|1571063117|WyqebJuR6uEYJNfsdiRHrnhsUi'
                         '/6mLnuKUYXLVRusi7Q4OlHy6qaiR5B9YHraiVTe2Lp2HoR3qoArdd6nRuHLA==; UTUSER=0; '
                         'l=cBMZyV2rqXNe1YpxBOCgVQKfuR_OtIRAguSJGtOBi_5ZL6L6JxbOkg_NPFp6cjWdt5Lp4NSLzt29-etl9AUGPSE9'
                         '-vNV.; isg=BNvb56IuAsfGRX6eXzOnKzR_aj_poIGTA50VI80YslrmrPGOVYWJATsuQmqHjEeq '
               }
    total_count = get_total(longitude, latitude, headers)
    if total_count == 0:
        return
    offset = 0
    while offset < total_count:
        # get_restauant(offset, header, latitude=latitude, longitude=longitude)
        get_restauant(offset, latitude=latitude, longitude=longitude, headers=headers)
        offset += 8
    for the_list in total_list:
        for restaurant in the_list:
            d = ['', '', '', '', '', '', ]
            d[0] = restaurant['restaurant']['name']
            d[1] = restaurant['restaurant']['flavors'][0]['name']
            d[2] = restaurant['restaurant']['id']
            # d[3] = get_restaurant_name(d[2])
            d[3] = json.loads(restaurant['restaurant']['business_info'])['recent_order_num_display']
            d[4] = restaurant['restaurant']['longitude']
            d[5] = restaurant['restaurant']['latitude']
            restaurant_list.append(d)


if __name__ == '__main__':
    total_list = []
    restaurant_list = []
    # get_result(113.351075,23.160833)
    longitude_list = np.arange(112.758106, 115.420483, 0.018).tolist()
    latitude_list = np.linspace(22.205805, 23.963091, 100).tolist()
    for i in range(len(longitude_list)):
        j = 0
        while (j < len(latitude_list)):
            multiprocessing.Process(target=get_result(longitude_list[i], latitude_list[j])).start()
            multiprocessing.Process(target=get_result(longitude_list[i], latitude_list[j + 1])).start()
            multiprocessing.Process(target=get_result(longitude_list[i], latitude_list[j + 2])).start()
            multiprocessing.Process(target=get_result(longitude_list[i], latitude_list[j + 3])).start()
            multiprocessing.Process(target=get_result(longitude_list[i], latitude_list[j + 4])).start()
            multiprocessing.Process(target=get_result(longitude_list[i], latitude_list[j + 5])).start()
            multiprocessing.Process(target=get_result(longitude_list[i], latitude_list[j + 6])).start()
            multiprocessing.Process(target=get_result(longitude_list[i], latitude_list[j + 7])).start()
            multiprocessing.Process(target=get_result(longitude_list[i], latitude_list[j + 8])).start()
            multiprocessing.Process(target=get_result(longitude_list[i], latitude_list[j + 9])).start()
            print(i, j)
            j += 10

    name = ['店铺名字', '类别', 'id', '月销售', '经度', '纬度']
    # name = ['店铺名字', '类别', 'id', '地址', '日销售', '经度', '纬度']
    result = pd.DataFrame(columns=name, data=restaurant_list)
    result = result.drop_duplicates()
    result.to_csv("data.csv", encoding="utf-8")
    restaurant_name_list = []
    for i in range(len(restaurant_list)):
        multiprocessing.Process(target=get_restaurant_name(result.iloc[i, 2]))
        print(i)
    name_result = pd.DataFrame(data=restaurant_name_list)
    name_result.to_csv("name.csv", encoding="utf-8")
