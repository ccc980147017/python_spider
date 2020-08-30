import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
}

class AmazonSpider(object):
    def __init__(self,url,item):
        self.url = url
        self.item = item


    def get_html(self,url):
        response = requests.get(url,headers=headers)
        # print(response.status_code)
        if response.status_code == 200:
            e = etree.HTML(response.text)
            return e

    def parse_category(self,html):
        div_list = html.xpath('//div[@id="siteDirectory"]/div/div')[2:]
        for div in div_list:
            category_name = div.xpath('./div[2]/div/div/div/span/a/text()')
            li_list = div.xpath('./div[2]/div/div/div/div/ul/li')
            for li in li_list:
                small_category = li.xpath('./span/span/a/text()')[0]
                small_category_url = li.xpath('./span/span/a/@href')[0]
                item[small_category] = small_category_url

    def parse_good(self,url):
        pass

    def parse_list(self,url):
        html = self.get_html(url)
        li_list = html.xpath('//div[@id="mainResults"]/ul/li')
        for li in li_list:
            good_name = li.xpath('./div/div[3]/div/a/h2/text()')[0]
            good_url = li.xpath('./div/div[3]/div/a/@href')[0]
            print(good_name)
            self.parse_good(good_url)
        try:
            next_url = html.xpath('//div[@id="pagn"]//a[@id="pagnNextLink"]/@href')[0]
            next_url = 'https://www.amazon.cn' + next_url
            if next_url:
                self.parse_list(next_url)

        except Exception:
            pass

    def start(self):
        html = self.get_html(self.url)
        self.parse_category(html)
        url = (url for url in item.values())
        for list_url in url:
            list_url = 'https://www.amazon.cn' + list_url
            self.parse_list(list_url)




if __name__ == '__main__':
    start_url = 'https://www.amazon.cn/gp/site-directory?ie=UTF8&ref_=nav_shopall_btn'
    item = {}
    a = AmazonSpider(start_url,item)
    a.start()
