from urllib.parse import urlencode,unquote,quote
import re,json,requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

#需要做好反反爬机制，变化ip
#搜索关键词 ajax接口获取数据
def parse(url):
    product = {}
    resposne = requests.get(url,headers=headers)
    json_data = json.loads(resposne.text)
    lis = json_data['data']['content']['offerResult']
    for item in lis:
        product['title'] = item['title']
        product['shop'] = item['loginId']
        product['price'] = item['strPriceMoney']
        product['img'] = item['imgUrl']
        print(product)


def spider():

    #搜索关键词
    keyword = '短裤'
    base_url = 'https://data.p4psearch.1688.com/data/ajax/get_premium_offer_list.json?'
    
    #page 也页码数，一般可以有100页
    #每一页有6个zpage
    for page in range(100):
        for zpage in range(6):
            params = {
                'beginpage':page + 1,
                'asyncreq' : zpage + 1,
                'keywords' : quote(keyword)
            }
            url = base_url + urlencode(params)
            # print(url)
            parse(url)

if __name__ == '__main__':
    spider()
