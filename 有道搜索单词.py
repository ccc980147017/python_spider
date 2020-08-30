import requests,random,json,re
from lxml import etree
import pprint

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

keyword = input('请输入要搜索的单词')

url = 'http://dict.youdao.com/w/{}/'.format(str(keyword))

response = requests.get(url,headers=headers)
e = etree.HTML(response.text)
try:
    scource = e.xpath('//div[@id="phrsListTab"]/div[@class="trans-container"]/ul/li/text()')[0]
    info_scoure_4 = e.xpath('//div[@id="tWebTrans"]/div[1]/div/span/text()')[0].strip()
    info_scoure_1 = e.xpath('//div[@id="tWebTrans"]/div[2]/div/span/text()')[0].strip()
    info_scoure_2 = e.xpath('//div[@id="tWebTrans"]/div[3]/div/span/text()')[0].strip()
    info_scoure_3 = e.xpath('//div[@id="tWebTrans"]/div[4]/div/span/text()')[0].strip()

    # duanju_1 = e.xpath('//div[@id="webPhrase"]/p[1]/span/a/text()')[0]
    # duanju_ch_1 = e.xpath('//div[@id="webPhrase"]/p[2]/text()')[0].strip()
    # duanju_2 = e.xpath('//div[@id="webPhrase"]/p[2]/span/a/text()')[0]
    # duanju_3 = e.xpath('//div[@id="webPhrase"]/p[3]/span/a/text()')[0]

    duan_ju_ch_1 = ''
    duan_ju_ch_2 = ''
    duan_ju_ch_3 = ''
    duan_ju_en_1 = ''
    duan_ju_en_2 = ''
    duan_ju_en_3 = ''
    try:
        p = re.compile(r'dict.basic.wordgroup">(.*?)</a></span>(.*?)</p>',re.S)
        duan_ju_en_1 = p.findall(response.text)[0][0]
        duan_ju_ch_1 = p.findall(response.text)[0][1].replace('\n                                                                                ','').replace('\n                                                ','')

        duan_ju_en_2 = p.findall(response.text)[1][0]
        duan_ju_ch_2 = p.findall(response.text)[1][1].replace('\n                                                                                ','').replace('\n                                                ','')

        duan_ju_en_3 = p.findall(response.text)[2][0]
        duan_ju_ch_3 = p.findall(response.text)[2][1].replace('\n                                                                                ','').replace('\n                                                ','')
    except Exception:
        pass

    # zhaoju_1 = e.xpath('//div[@class="trans-content"]//div[@class="examples"]/p[1]/text()')[0]
    # zhaoju_ch_1 = e.xpath('//div[@class="trans-content"]//div[@class="examples"]/p[2]/text()')[0]
    item = {}

    item['搜索关键字'] = keyword
    item['解释'] = scource
    item['其他解释1'] = info_scoure_4
    item['其他解释2'] = info_scoure_1
    item['其他解释3'] = info_scoure_2
    item['其他解释4'] = info_scoure_3
    item['短句1'] = duan_ju_en_1 + '   中文：'+ duan_ju_ch_1
    item['短句2'] = duan_ju_en_2 + '   中文：'+ duan_ju_ch_2
    item['短句3'] = duan_ju_en_3 + '   中文：'+ duan_ju_ch_3

    print(json.dumps(item, ensure_ascii=False, indent=4))



except Exception as e:
    print('您搜索的单词不存在')
#     print(e)

end = input('输入exit退出')
if end == 'exit':
    print(exit())
else:
    print('输入有误')




