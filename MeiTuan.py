# coding=utf-8
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup


# 区域店铺id ct_Poi cateName抓取，传入参数为区域id
def crow_id(areaid):
    url = 'https://meishi.meituan.com/i/api/channel/deal/list'
    head = {'Host': 'meishi.meituan.com',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://meishi.meituan.com/i/?ci=30&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Mobile Safari/537.36',
            'Cookie': '__mta=50254617.1569252852580.1570694007455.1570694257790.53; wm_order_channel=default; '
                      'utm_source=; _lxsdk_cuid=16d5eb74af6c8-07a0da65a2a5f9-67e1b3f-1fa400-16d5eb74af7c8; '
                      '_hc.v=56466f70-ff6d-6c0d-2f05-d2108518d1ef.1569252624; '
                      'iuuid=236A75312BAD4B7D41DE4758E9D7723AF9B08BA0982CB11A5FA8B4A12867C8EA; '
                      '_lxsdk=236A75312BAD4B7D41DE4758E9D7723AF9B08BA0982CB11A5FA8B4A12867C8EA; webp=1; rvct=20%2C30; '
                      'cityname=%E5%B9%BF%E5%B7%9E; cssVersion=f70c15b3; au_trace_key_net=default; '
                      'openh5_uuid=236A75312BAD4B7D41DE4758E9D7723AF9B08BA0982CB11A5FA8B4A12867C8EA; '
                      'client-id=c5dd1783-a1a4-4beb-8c84-89550b00bb8a; IJSESSIONID=13hzbs6t9mona1khmcauxhorpz; ci=20; '
                      'logan_custom_report=; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; ci3=1; '
                      '__utmc=74597006; meishi_ci=20; cityid=20; '
                      'UM_distinctid=16db470b6454ad-018dc240759bb9-67e1b3f-1fa400-16db470b64675c; '
                      'CNZZDATA1256793290=1110896055-1570689798-%7C1570689798; backurl=https://i.meituan.com; '
                      'mtcdn=K; __utma=74597006.1799448388.1569252788.1570690259.1570692362.6; '
                      '__utmz=74597006.1570692362.6.6.utmcsr=meishi.meituan.com|utmccn=('
                      'referral)|utmcmd=referral|utmcct=/i/; isid=DADB35D25C8CEC4499382637104EB8CD; '
                      'oops=yNxrWAnp-C5UQ3VELgq72McoaRcAAAAAPAkAAAaAPwJtmLo6QTKdkD7S5ctf4TVqwsErLx3HnDyBlE'
                      '-8l3e059CKa7v8z2IEr9WUaw; logintype=fast; '
                      'p_token=yNxrWAnp-C5UQ3VELgq72McoaRcAAAAAPAkAAAaAPwJtmLo6QTKdkD7S5ctf4TVqwsErLx3HnDyBlE'
                      '-8l3e059CKa7v8z2IEr9WUaw; uuid=c858cc0887ce461fbdbf.1570693975.1.0.0; u=1196961380; '
                      'latlng=23.161997,113.36211,1570693987599; __utmb=74597006.8.9.1570693988188; '
                      'i_extend=C_b1Gimthomepagecategory11H__a; logan_session_token=gsfw4qdkegopn7vrmluy; '
                      '_lxsdk_s=16db45ee332-a5c-2e6-b0f%7C%7C185 '
            }
    data = {"uuid": "c858cc0887ce461fbdbf.1570693975.1.0.0", "version": "8.3.3", "platform": 3, "app": "",
            "partner": 126, "riskLevel": 1, "optimusCode": 10,
            "originUrl": "http://meishi.meituan.com/i/?ci=30&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",
            "offset": 0, "limit": 15, "cateId": 21329, "lineId": 0, "stationId": 0, "areaId": areaid, "sort": "default",
            "deal_attr_23": "", "deal_attr_24": "", "deal_attr_25": "", "poi_attr_20043": "", "poi_attr_20033": ""}
    r = requests.post(url, headers=head, data=data)
    try:
        result = json.loads(r.text)
    except:
        print(r.text)
    totalcount = result['data']['poiList']['totalCount']  # 获取该分区店铺总数，计算出要翻的页数
    datas = result['data']['poiList']['poiInfos']
    for d in datas:
        d_list = ['', '', '', '', '', '']
        d_list[0] = d['name']
        d_list[1] = d['cateName']
        d_list[2] = d['poiid']
        d_list[3] = d['ctPoi']
        d_list[4] = d['lat']
        d_list[5] = d['lng']
        id_list.append(d_list)
    # 将数据保存到本地csv
    # with open('meituan_id.csv', 'a', newline='', encoding='gb18030')as f:
    #     write = csv.writer(f)
    #     for i in id_list:
    #         write.writerow(i)

    # 开始爬取第2页到最后一页
    offset = 0
    if totalcount > 15:
        totalcount -= 15
        while offset < totalcount:
            offset += 15
            # 构造post请求参数，通过改变offset实现翻页
            data2 = {"uuid": "c858cc0887ce461fbdbf.1570693975.1.0.0", "version": "8.3.3", "platform": 3, "app": "",
                     "partner": 126, "riskLevel": 1, "optimusCode": 10,
                     "originUrl": "http://meishi.meituan.com/i/?ci=30&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",
                     "offset": offset, "limit": 15, "cateId": 21329, "lineId": 0, "stationId": 0, "areaId": areaid,
                     "sort": "default",
                     "deal_attr_23": "", "deal_attr_24": "", "deal_attr_25": "", "poi_attr_20043": "",
                     "poi_attr_20033": ""}
            try:
                r = requests.post(url, headers=head, data=data2)
                result = json.loads(r.text)
                datas = result['data']['poiList']['poiInfos']
                for d in datas:
                    d_list = ['', '', '', '', '', '']
                    d_list[0] = d['name']
                    d_list[1] = d['cateName']
                    d_list[2] = d['poiid']
                    d_list[3] = d['ctPoi']
                    d_list[4] = d['lat']
                    d_list[5] = d['lng']
                    id_list.append(d_list)
                # 保存到本地
            except:
                pass


def get_restaurant_name(poiid, ctPoi):
    url = "http://meishi.meituan.com/i/poi/" + str(poiid) + "?ct_poi=" + str(ctPoi)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/66.0.3359.139 Mobile Safari/537.36'}
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")


if __name__ == '__main__':
    id_list = []
    areaId_list = [23, 22, 274, 24, 26, 25, 737, 739, 738, 740, 1068]
    for i in range(len(areaId_list)):
        crow_id(areaId_list[i])
        print(len(id_list))
    name = ['店铺名字', '类别', 'poiid', 'ctPoi', '经度', '纬度']
    # name = ['店铺名字', '类别', 'id', '地址', '日销售', '经度', '纬度']
    result = pd.DataFrame(columns=name, data=id_list)
    result = result.drop_duplicates()
    result.to_csv("MeiTuanId.csv", encoding="utf-8")

    poiid = '180584081'
    ctPoi = '059343649361170105379968473281275637644_a180584081_c0_e2745027750983486858_nareaid23'
    url = "http://meishi.meituan.com/i/poi/" + poiid + "?ct_poi=" + ctPoi
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/66.0.3359.139 Mobile Safari/537.36'}
    r = requests.get(url, headers=headers)
