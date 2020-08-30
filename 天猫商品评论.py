# -*- coding: utf8 -*-
import requests
import simplejson
import json
import time
import random

#拿到商品评论的urlhttps://rate.tmall.com/list_detail_rate.htm?itemId=550177114361&spuId=719012436&sellerId=2291154335&order=1&append=0&content=1&tagId=&posi=&picture=&groupId=
#修改其中的参数 itemId   spuId  sellerId   order 就可以了
#但要注意反爬，会有滑块验证码

base_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=541181337628&spuId=418352337&sellerId=2291154335' \
           '&order=3&append=0&content=1&tagId=&posi=&picture=&groupId='
header = {'Connection': 'keep-alive',
          # 需要自行补充cookies
          'Cookie': '',
          'Referer': 'https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-14496201253.115.12a46424wwuz5U'
                     '&id=550177114361&rn=e7a9695a68263c726e040e64135c868d&abbucket=14&skuId=4466169090671',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/75.0.3770.100 Safari/537.36'}
#商品id
productId = ''

for i in range(1, 100, 1):
    url = base_url + '&currentPage=%s' % str(i)
    print(url)
    tb_req = requests.get(url, headers=header).text[11:-1]
   #将str格式的文本格式化为字典
    # print(tb_req)
    #print(len(tb_req))
    tb_dict = simplejson.loads(tb_req)

   #编码： 将字典内容转化为json格式对象
    tb_json = json.dumps(tb_dict, indent=2)   #indent参数为缩紧，这样打印出来是树形json结构，方便直观
   #解码： 将json格式字符串转化为python对象
    review_j = json.loads(tb_json)
    print('正在爬取第%s页'%str(i))

    for p in range(0, 20, 1):
        ys = [review_j["rateDetail"]["rateList"][p]['auctionSku'].encode('utf-8').decode('utf-8')]
        dat = [review_j["rateDetail"]["rateList"][p]['rateDate'].encode('utf-8').decode('utf-8')]
        pl = [review_j["rateDetail"]["rateList"][p]['rateContent'].encode('utf-8').decode('utf-8')]
        nam = [review_j["rateDetail"]["rateList"][p]['displayUserNick'].encode('utf-8').decode('utf-8')]
        zp = [review_j["rateDetail"]["rateList"][p]['appendComment']]
        if zp == [None]:
            zp = zp
        else:
            zp = [review_j["rateDetail"]["rateList"][p]['appendComment']['content'].encode('utf-8').decode('utf-8')]
        item = {}
        item['ys'] = ys
        item['pl'] = pl
        print(item)

    time.sleep(random.uniform(2.5, 3))

print('Done!')

