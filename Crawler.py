import json
import requests
import pandas as pd
import numpy as np
import time
from threading import Thread

def get_restauant(offset, longitude, latitude):
    url = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude=' + str(latitude) + '&longitude=' + str(
        longitude) + '&keyword=&offset=' + str(
        offset) + '&limit=8&extras[]=activities&extras[' \
                  ']=tags&terminal=h5&rank_id=222dafdcdd9a447e97375ce485f3e2ad&brand_ids[' \
                  ']=&restaurant_category_ids[]=-102 '
    header = {'Accept': 'application/json, text/plain, */*',
              'Referer': 'https://h5.ele.me/msite/food/',
              'Sec-Fetch-Mode': 'cors',
              'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                            'like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36',
              'X-Shard': 'loc=113.370711,23.153689, loc=113.370711,23.153689',
              'x-uab': '120#bX1bSwFgN2f2oaGKhLhMgVU//Gf/ijkxqEqkC0oVDQIMq7wWHHidl2dAh360gv3LWHGZusBg/d7uL6E8xmGlHDn0Aw'
                       '+O3ztdMoed4Bbq9JHAM2UlfTWKife2HiUQGRvCbjcyknLFlAPs0l7Saz+bNFYvSi5/ybbS7UGPWWl/oYk6y3b9wg'
                       '+eavxYg6ikMx3xPrqwXJGqcp5pZOCcYoA8jPH9L7q6E5phfCPg8+JvnFBZ2zTQ6kl6YlEsE05bUUJ'
                       '/mHsWCRmGGXqmC7RVLFr33MuQky7YWo+CN1hQADWok9x0obdbGEOJigdSAznx92XsCMJUdToiO22D+Zjq'
                       '/6j9MhVXRotmcJ7ixoU5nz6UCE55WfnjGZGzG1AWX2f7AxtJnKuBaJgQZbKp3FEJ0jVuzWH7rYZKnXsvhWHLps2G'
                       '+gJCeEcIVJl4YZ1RwStZiFsJNRllkVG7hx8F3mD5XvrAOeMu6Ebw3vHmnOFm0RnIvQ7DpYRuS77hFYQ7KpBGQpNzpjj0UgwejHXL5hgPkcGG8F0O6QMLSRf/r27yPmZ9+x9p28qjRLcr0ytIuAACt7icMa2oyr4nSYXrbr5Xn7GTXtTsm+Z7tQcw9jE1ECUz6b4Dz4Tpw80mN3da3RoSuwVRPy+LJBvkVXAntjv3QqlalvnzluPwlByeNISivYbT3mX6ewElt9Ji90C4/MueKE5/UBa/yKCGGJ8gAE0n055rVn8s+5dOYxRcw/NhOuJMmsK5uDRTbJud94yEaqO6N+4r5LBrESVlafCirqfhp+9RJ8eY3v3FQXT804Yn0jRJ5NmL8kh3FOjWfeCZgBhiVtmEtMGmkbXU4gJXPlYyom5PictYncAYmg6/Acrc9lBSlGz08IbbjPOHK5pIBylXcxVX49rR4dpm2Y7sMg40rgHKCkjWKH7IjAfMmSbZMVqqv5uEyckI3QbTeFkDCv8ZpA60Fd5vM7kqxty8ZBrxbP+NXiTW/uwNWOzb30KsIdX3Do2Hj/LFexSqdCrbUkeOiSZqP5xw1lH2LkU9+MlJeZ0l9kVNReOWuuUxQs7b/SHeKFdePdE8/dxT67EqnFIHTQsO8WvnHvG0y6ycm8LRkpwE5j2mwGpHWivwWcn+7itZ/6wQk/M25+WdibN58USWLvxrQIpahRbChh/PUsdu9DEsrj43aQTooDdoGkix02CnufMqL1JjnOluLxgUvtw721SqgK22iidxBDDdKOD4e3qNqbMXie15wwLu7gXfDsarQqyZ5CG3pAAgn7H0s+rYELMAkXJ8c6L5bXR55uS7duUtcgUZTy/aL5O9nBgrCtwFqSV8DXhcyHTlbWSQ74QCoaxVOke0kN6+lZBdf4B/J7jTGmlwQ8MxtRD0cEENs6MdTYtEk1fmBjwUV7I2MPfnOoSlFrVfMYI0juiYcJa9dyOUQ/Ii/nsa/uXQzDPh2ES7sQycywZXBnIBwpg5fBRnjF4+rjF+9JPZA5i04Mh3ziF1SIwI9zox0PXUtjvo5GGm+xDrdYQ4QGtFtmhW59XTdYwVbVqfi0EIYRz3I4/7ab7Wx5h/8pT9dN5XMigBv/GaB1A9LSlGivROsJhpHllbBW7a+F9l+WgvgHOHyUYAYOMIrYG9TDCqp647HA+CKV7wXpkgGGYVtzDJAQYCBmm2tMnBvGeD9xwRMHgCcofZfQw1NzNx5rBW3HF1DVgQkZayNoYIPlwr+D70SgxPJ1xPXE2Em8xArHrO7JtTkbtZzltGAdUvD6/FzCi1dcy4CxjlR0LK5ibMuEAfnDAjSUGdy60vG5GTJCqpnj84CMHmYDizhRJy9qp5cyOpav/q6Hrg+E7oc1yfkGBtERU7RL9VQophJ433Pwz9IzFwztA7rqaIPA+fVvCK9YG4/6/VIw79MJEZcru0wy9PJX8V8kwSDl5+NoyeaI== ',
              'cookie': 'ubt_ssid=cmqbrw0dditxri4uohu24duie4xa8qnk_2019-09-23; cna=5dWkFbfoOy8CAX1YGIrG6fe6; _utrace=88d11b084d20ec888553b1da0026c8eb_2019-09-23; ut_ubt_ssid=sx8kew8r4if9eq9225ozjm7dul6g7u42_2019-09-23; perf_ssid=nyu3zm5xqa8lc2nwabzqtmhv574lhxlo_2019-09-23; track_id=1569251986|b2b4bf1e89411d9fe0e5cd50e46456141740833ac43b7a0b2a|ce3ff3e71aa873a9460122dad833d050; USERID=2014785793; tzyy=c509115f45309f970d4abe0e479d95bb; _bl_uid=9skUz1bp4q5xeLob244kka6m5zpF; SID=67gYakyp1idL49Ou5PhCoPJfGgvuD43fk4hQ; ZDS=1.0|1570435491|qdycxJnlCYN3HeOY2DyM6B41HDqpZ3B4SF+ZECpxJotUpohjlg8OANrFvorAeozvZ38ksGYxXEMqpWi6f5LpZg==; pizza73686f7070696e67=_HHDoSEnvf2VhWkyuKdvCYeibEGnRIjUv4bLjabtKpAmIOASNNM6bOFsaQi8tYqo; l=cBMZyV2rqXNe1EIiBOfalurza7792IRb4sPzaNbMiICPOUfk5ZMFWZBaj08DCnGVp6IHJ3Wm0ejuBeYBqMd3lC81piV3p; UTUSER=0; isg=BDk51e5zQLJ2QRw0KWUlsZoxSKUTRi34uLxXq1tutWDf4ll0o5Y9yKczYKCx2sUw'
              }
    r = requests.get(url, headers=header)
    result = json.loads(r.text)
    try:
        restaurant_list = result['items']
        total_list.append(restaurant_list)
    except:
        print(result)
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
    header = {
        'cookie': 'ubt_ssid=cmqbrw0dditxri4uohu24duie4xa8qnk_2019-09-23; cna=5dWkFbfoOy8CAX1YGIrG6fe6; _utrace=88d11b084d20ec888553b1da0026c8eb_2019-09-23; ut_ubt_ssid=sx8kew8r4if9eq9225ozjm7dul6g7u42_2019-09-23; perf_ssid=nyu3zm5xqa8lc2nwabzqtmhv574lhxlo_2019-09-23; track_id=1569251986|b2b4bf1e89411d9fe0e5cd50e46456141740833ac43b7a0b2a|ce3ff3e71aa873a9460122dad833d050; USERID=2014785793; tzyy=c509115f45309f970d4abe0e479d95bb; _bl_uid=9skUz1bp4q5xeLob244kka6m5zpF; SID=67gYakyp1idL49Ou5PhCoPJfGgvuD43fk4hQ; ZDS=1.0|1570435491|qdycxJnlCYN3HeOY2DyM6B41HDqpZ3B4SF+ZECpxJotUpohjlg8OANrFvorAeozvZ38ksGYxXEMqpWi6f5LpZg==; pizza73686f7070696e67=_HHDoSEnvf2VhWkyuKdvCYeibEGnRIjUv4bLjabtKpAmIOASNNM6bOFsaQi8tYqo; l=cBMZyV2rqXNe1EIiBOfalurza7792IRb4sPzaNbMiICPOUfk5ZMFWZBaj08DCnGVp6IHJ3Wm0ejuBeYBqMd3lC81piV3p; UTUSER=0; isg=BDk51e5zQLJ2QRw0KWUlsZoxSKUTRi34uLxXq1tutWDf4ll0o5Y9yKczYKCx2sUw'}
    total_count = get_total(longitude, latitude, header)
    if total_count == 0:
        return
    offset = 0
    while offset < total_count:
        # get_restauant(offset, header, latitude=latitude, longitude=longitude)
        get_restauant(offset, latitude=latitude, longitude=longitude)
        offset += 8
    for the_list in total_list:
        for restaurant in the_list:
            d = ['', '', '', '', '', '', ]
            d[0] = restaurant['restaurant']['name']
            d[1] = restaurant['restaurant']['flavors'][0]['name']
            d[2] = restaurant['restaurant']['id']
            # d[3] = get_restaurant_name(d[2])
            d[3] = "".join(fil(json.loads(restaurant['restaurant']['business_info'])['recent_order_num_display']))
            d[4] = restaurant['restaurant']['longitude']
            d[5] = restaurant['restaurant']['latitude']
            restaurant_list.append(d)


if __name__ == '__main__':
    total_list = []
    restaurant_list = []
    # get_result(113.351075,23.160833)
    longitude_list = np.linspace(113, 127).tolist()
    latitude_list = np.linspace(23, 46).tolist()

    try:
        for longitude in longitude_list:
            for latitude in latitude_list:
                print(longitude, latitude)
                get_result(longitude, latitude)
                print(len(restaurant_list))
                time.sleep(2)
    finally:
        name = ['店铺名字', '类别', 'id', '日销售', '经度', '纬度']
        # name = ['店铺名字', '类别', 'id', '地址', '日销售', '经度', '纬度']
        result = pd.DataFrame(columns=name, data=restaurant_list)
        result.to_csv('data.csv', encoding='gbk')
