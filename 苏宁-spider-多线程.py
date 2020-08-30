import requests,json,time,re,os,csv
from lxml import etree
import threading,queue

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

# 商品价格页的 地址
price_url = 'https://icps.suning.com/icps-web/getVarnishAllPriceNoCache/0000000%s_010_0100101_0000000000_1_getClusterPrice.jsonp?callback=getClusterPrice'


def parse_datail(url,item):

    response = requests.get(url,headers=headers)
    e = etree.HTML(response.text)

    brand = e.xpath('//div[@class="breadcrumb"]/div[3]/span/a/text()')[0]
    model = e.xpath('//span[@class="breadcrumb-title"]/a/text()')[0]
    # price = e.xpath('//div[@id="priceDom"]//span[@class="mainprice"]/i/text()')[0]
    item['brand'] = brand
    item['model'] = model
    # item['price'] = price


def parse_price(id,item):
    full_url = price_url%(id)
    response = requests.get(full_url,headers=headers)
    text = response.text
    price_info = re.match('.*getClusterPrice\(?(.+)\).*', text, re.S).group(1)
    price = json.loads(price_info)[0]['price']
    price = float(price) if price else 0.0
    # print(price)

def save_to_csv(item):
    base_dir = '结果文件'
    if not os.path.isdir(base_dir):
        os.makedirs(base_dir)
    file_path = base_dir + os.sep + str(keyword) + '.csv'
    if not os.path.isfile(file_path):
        is_first_write = 1
    else:
        is_first_write = 0
    if item:
        with open(file_path, 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            if is_first_write:
                header = ['id','product_name','info_url','comment_num','shop_name','brand','model']
                writer.writerow(header)
            writer.writerow([item[key] for key in item.keys()])
    print('写入成功')

def main(url_queue):


    # print(page,layer)

    # 商品价格页的 地址
    price_url = 'https://icps.suning.com/icps-web/getVarnishAllPriceNoCache/0000000%s_010_0100101_0000000000_1_getClusterPrice.jsonp?callback=getClusterPrice'

    while not url_queue.empty():
        full_url = url_queue.get()
        response = requests.get(full_url,headers=headers)
        item = {}
        # print(response.text)
        if response.status_code == 200:
            # try :
            e = etree.HTML(response.text)
            good_list = e.xpath('//body/li')
            for li in good_list:
                try:
                    # id = li.xpath('.[@id]')
                    id = li.xpath('.//div[@class="product-box "]/div[3]/a[1]/@id')[0]
                    title = li.xpath('.//div[@class="title-selling-point"]/a/@title')[0]
                    info_url = 'http:' + li.xpath('.//div[@class="title-selling-point"]/a/@href')[0]
                    comment_num = li.xpath('.//div[@class="info-evaluate"]/a/i/text()')[0]
                    shop_name = li.xpath('.//div[@class="store-stock"]/a/text()')[0]

                    item['id'] = id
                    item['title'] = title
                    item['info_url'] = info_url
                    item['comment_num'] = comment_num
                    item['shop_name'] = shop_name
                except Exception :
                    # print(info_url)
                    pass


            parse_datail(info_url,item)
            parse_price(id,item)
            print(item)
            save_to_csv(item)

if __name__ == '__main__':
    # 商品列表页的 初始页
    page = 0

    # 商品列表页的 层数
    layer = 0
    # 需要爬取的 类目
    keyword = input('请输入你要爬取的关键词：')

    url_queue = queue.Queue()

    # 商品列表页的 地址
    url = 'https://search.suning.com/emall/searchV1Product.do?keyword={0}&pg=01&cp=%d&paging=%d'.format(keyword)

    # 判断 商品列表页 层数 并 回调 parse函数（处理商品列表页函数）

    while layer < 3 and page < 50:
        layer += 1
        full_url = url %(page,layer)
        url_queue.put(full_url)
        # print(url_queue.get())
        if layer == 3:
            break

    #layer=paging  page=cp
    # while layer == 3 and page < 49:
    while True:
        layer = 0
        page += 1
        full_url = url %(page,layer)
        url_queue.put(full_url)
        if page == 50:
            break

    # print(url_queue.qsize())
    print(url_queue.qsize())

    t1 = threading.Thread(target=main,args=(url_queue,))
    t1.start()

    t2 = threading.Thread(target=main,args=(url_queue,))
    t2.start()

