import execjs,requests,json

headers = {
    'referer': 'https://fanyi.baidu.com/?aldtype=16047',
    'cookie': 'REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BAIDUID=07E708BF231B0965C1AD56311434CAF3:FG=1; PSTM=1593347840; BIDUPSID=3B0C5E74173D804518BA50A4048C24FB; BDUSS=kRreUUwYlUzSXk4SVV1QVZuc3NMSWV4SUJ5UnBOd2RUQUxvN05OTEw5aldrVFpmSVFBQUFBJCQAAAAAAAAAAAEAAADYbvRlQ2hyb21lODc5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANYED1~WBA9fQ; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS_BFESS=kRreUUwYlUzSXk4SVV1QVZuc3NMSWV4SUJ5UnBOd2RUQUxvN05OTEw5aldrVFpmSVFBQUFBJCQAAAAAAAAAAAEAAADYbvRlQ2hyb21lODc5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANYED1~WBA9fQ; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1596955137,1597329890; delPer=0; PSINO=7; H_PS_PSSID=1465_32569_31660_32046_32394_32407_32117_32090_26350_32496_32482_22158; yjs_js_security_passport=e69c1f8fe4402dcef9b419fc585aa8e7117db39f_1597667399_js; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1597667510; __yjsv5_shitong=1.0_7_43f146b173faffb244d90f9f34aad21acbc3_300_1597667516984_14.127.248.166_31da2e41',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}
node = execjs.get()
file = '百度翻译.js'
ctx = node.compile(open(file,encoding='utf-8').read())

#翻译关键词
keyword = 'python'
js = "get_sign('{}')".format(keyword)

sign = ctx.eval(js)
# print(sign)

data = {
    'from': 'en',
    'to': 'zh',
    'query': keyword,
    'transtype': 'realtime',
    'simple_means_flag': '3',
    'sign': str(sign),
    'token': 'd1c4aa16c548d1bf7d72f1dc5a53f5c4',
    'domain': 'common'
}
url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
response = requests.post(url,headers=headers,data=data)
print(response.json())

