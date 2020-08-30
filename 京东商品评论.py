# -*- coding: utf8 -*-
import requests
import simplejson
import json
import time
import pymysql
import random


base_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv56' \
           '&productId=3973338&score=0&sortType=6&pageSize=10&isShadowSku=0&fold=1'
header = {'Connection': 'keep-alive',
          #需要自行补充cookies
          'Cookie': '',
          'Referer': 'https://item.jd.com/3973338.html'}

for i in range(21,100,1):
    url = base_url + '&page=%s' % str(i)
   # 将响应内容的文本取出
    tb_req = requests.get(url, headers=header).text[24:-2]
   #print(tb_req)
   #将str格式的文本格式化为字典
    print(tb_req)
    tb_dict = simplejson.loads(tb_req)
   #编码： 将字典内容转化为json格式对象
    tb_json = json.dumps(tb_dict, indent=3)   #indent参数为缩紧，这样打印出来是树形json结构，方便直观

   #解码： 将json格式字符串转化为python对象
    review_j = json.loads(tb_json)
    for p in range(0, 10, 1):
        pl = [review_j["comments"][p]['content'].encode('utf-8').decode('utf-8')]
        sc = [review_j["comments"][p]['score']]
        ys = [review_j["comments"][p]['productColor'].encode('utf-8').decode('utf-8')]
        name = [review_j["comments"][p]['nickname'].encode('utf-8').decode('utf-8')]
        dat = [review_j["comments"][p]['creationTime'].encode('utf-8').decode('utf-8')]
        zp = [review_j["comments"][p]['afterDays']]

        if zp == [0]:
            zp = None
        else:
            zp = [review_j["comments"][p]['afterUserComment']
                  ['hAfterUserComment']['content'].encode('utf-8').decode('utf-8')]

    time.sleep(random.uniform(2.5, 5))
print('Done!')

