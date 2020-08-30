import json
import requests
import datetime
import simplejson
import time

for j in range(1, 20):

    postUrl = 'https://www.xiaomiyoupin.com/mtop/market/comment/product/content'
    # payloadData数据
    payloadData = {
        'folding': False,
        'gid': 112825,
        'pindex': j,
        'psize': 10,
        'source': 'PC',
        'tag_id': 0,
        'tag_name': '全部'
    }
    # 请求头设置
    payloadHeader = {
        'Host': 'www.xiaomiyoupin.com',
        'Content-Type': 'application/json',

        #需要自行补充cookies
        'cookie': '',
        'referer': 'https://www.xiaomiyoupin.com/detail?gid=112825&spmref=YouPinPC.$undefined$.search_list.3.93905513'
    }
    # 下载超时
    timeOut = 25

    r = requests.post(postUrl, data=json.dumps(payloadData), headers=payloadHeader)
    dumpJsonData = json.dumps(payloadData)
    print(f"dumpJsonData = {dumpJsonData}")

    res = requests.post(postUrl, data=dumpJsonData, headers=payloadHeader, timeout=timeOut, allow_redirects=True)
    print(f"responseTime = {datetime.datetime.now()}, statusCode = {res.status_code}, res text = {res.text}")
    response = res.text
    review = simplejson.loads(response)

    for i in range(0, 10):
        #爬取评论时间
        yp_time = review['data']['list'][i]['ctime']
        timeArray = time.localtime(yp_time)
        #爬取评论者昵称
        nick_name = review['data']['list'][i]['nick_name']
        #爬取小米有品评论
        content = review['data']['list'][i]['txt']
        #爬取评论星级
        star = review['data']['list'][i]['score']
        # cursor.execute(sql_insert, (timeArray, nick_name, content, star))
        # db.commit()

        item = {}
        item['time'] = timeArray
        item['comment'] = content
        print(item)
    time.sleep(10)
        # print(content)
db.close()
