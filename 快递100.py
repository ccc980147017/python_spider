import requests,random,json,random
from lxml import etree

headers = {
    'Referer': 'https://www.kuaidi100.com/?from=openv',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
num = random.random()

#快递单号
postid = ''

get_company_url = 'https://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text={}'.format(postid)
response = requests.post(get_company_url,headers=headers)

json_data = response.json()
type = json_data['auto'][0]['comCode']

url = 'https://www.kuaidi100.com/query?type={}&postid={}&temp={}&phone='.format(str(type),postid,num)

response = requests.get(url,headers=headers).json()
# response = requests.get(url,headers=headers,proxies=proxy).json()
# print(response)

data_list = response['data']
for data in data_list:
    time = data['time']
    context = data['context']
    print(time,context)


