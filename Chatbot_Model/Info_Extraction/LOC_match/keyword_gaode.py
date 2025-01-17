# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     keyword_gaode.py
   Description :   利用关键字查询poi
   Author :       charl
   date：          2018/9/7
-------------------------------------------------
   Change Activity: 2018/9/7:
-------------------------------------------------
"""

import json
import xlwt
import pprint

from urllib.parse import quote
from urllib import request

amap_web_key = '85d3ed3aceaf0a259f81d5ae47a32e59'
poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"

# 根据关键词获取poi数据
def getpois(keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(keywords, i)
        result = json.loads(result)  # 将字符串转换为json
        if result['count'] == '0':
            break
        hand(poilist, result)
        i = i + 1
    return poilist

def hand(poilist, result):
    '''
    将返回的数据装入集合返回
    :param poilist:
    :param result:
    :return:
    '''
    pois = result['pois']
    # for i in range(len(pois)):
    #     poilist.append(pois[i])
    poilist.append(pois[0])

def getpoi_page(keywords, page):
    '''
    单页获取pois
    :param keywords:
    :param page:
    :return:
    '''
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
        keywords) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data

def getBoundById(id):
    '''
    根据id获取边界数据
    :param id:
    :return:
    '''
    req_url = poi_boundary_url + "?id=" + id
    with request.urlopen(req_url) as f:
        data = f.read()
        dataList = []
        datajson = json.loads(data)  # 将字符串转换为json
        datajson = datajson['data']
        datajson = datajson['spec']
        if len(datajson) == 1:
            return dataList
        if datajson.get('mining_shape') != None:
            datajson = datajson['mining_shape']
            shape = datajson['shape']
            dataArr = shape.split(';')

            for i in dataArr:
                innerList = []
                f1 = float(i.split(',')[0])
                innerList.append(float(i.split(',')[0]))
                innerList.append(float(i.split(',')[1]))
                dataList.append(innerList)
        return dataList

def get_detail_info(keyword):
    '''
    获取详细信息
    :param keyword: 传入的关键词
    :return:
    '''
    result = {}
    pois = getpois(keyword)

    # for i in range(len(pois)):
    # 只取第0个数据
    name = pois[0]['alias']  # 别名
    location = pois[0]['entr_location']   # 经纬度
    addr = pois[0]['pname'] + pois[0]['cityname'] + pois[0]['adname'] + pois[0]['address']   # 详细地址拼接
    result['addr'] = addr
    result['location'] = location
    result['name'] = name
    # pprint.pprint(result)
    # pprint.pprint(len(pois))
    return result

keyword = "迪凯国际中心"
# pois = getpois(keyword)
# pprint.pprint(pois)

if __name__ == "__main__":
    get_detail_info(keyword)


