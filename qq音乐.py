import requests,os,click
from contextlib import closing
import random,json

'''清楚可能出问题的字符'''
def filterBadCharacter(string):
	string = string.replace('<em>', '').replace('</em>', '') \
				   .replace('<', '').replace('>', '').replace('\\', '').replace('/', '') \
				   .replace('?', '').replace(':', '').replace('"', '').replace('：', '') \
				   .replace('|', '').replace('？', '').replace('*', '')
	return string.strip().encode('utf-8', 'ignore').decode('utf-8')

'''秒转时分秒'''
def seconds2hms(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	return '%02d:%02d:%02d' % (h, m, s)

def main(keyword):
    search_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
    mobile_fcg_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg'
    fcg_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
    ios_headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        'Referer': 'http://y.qq.com'
        }

    session = requests.Session()
    params = {
        'w': keyword,
        'format': 'json',
        'p': '1',
        'n': 5
        }

    response = session.get(search_url, headers=headers, params=params)
    # print(response.json())

    all_items = response.json()['data']['song']['list']
    songinfos = []
    for item in all_items:
        params = {
                    'guid': str(random.randrange(1000000000, 10000000000)),
                    'loginUin': '3051522991',
                    'format': 'json',
                    'platform': 'yqq',
                    'cid': '205361747',
                    'uin': '3051522991',
                    'songmid': item['songmid'],
                    'needNewCode': '0'
                }
        ext = ''
        download_url = ''
        filesize = '-MB'

        for quality in [("A000", "ape", 800), ("F000", "flac", 800), ("M800", "mp3", 320), ("C400", "m4a", 128), ("M500", "mp3", 128)]:
            params['filename'] = '%s%s.%s' % (quality[0], item['songmid'], quality[1])
            response = session.get(mobile_fcg_url, headers=ios_headers, params=params)
            response_json = response.json()
            # print(response_json)

            if response_json['code'] != 0: continue
            vkey = response_json.get('data', {}).get('items', [{}])[0].get('vkey', '')
            if vkey:
                ext = quality[1]
                download_url = 'http://dl.stream.qqmusic.qq.com/{}?vkey={}&guid={}&uin=3051522991&fromtag=64'.format('%s%s.%s' % (quality[0], item['songmid'], quality[1]), vkey, params['guid'])
                if ext in ['ape', 'flac']:
                    filesize = item['size%s' % ext]
                elif ext in ['mp3', 'm4a']:
                    filesize = item['size%s' % quality[-1]]
                break

        if not download_url:
            params = {
                        'data': json.dumps({
                                            "req": {"module": "CDN.SrfCdnDispatchServer", "method": "GetCdnDispatch", "param": {"guid": "3982823384", "calltype": 0, "userip": ""}},
                                            "req_0": {"module": "vkey.GetVkeyServer", "method": "CgiGetVkey", "param": {"guid": "3982823384", "songmid": [item['songmid']], "songtype": [0], "uin": "0", "loginflag": 1, "platform": "20"}},
                                            "comm": {"uin": 0, "format": "json", "ct": 24, "cv": 0}
                                        })
                    }
            response = session.get(fcg_url, headers=ios_headers, params=params)
            response_json = response.json()
            # print(response_json)

            if response_json['code'] == 0 and response_json['req']['code'] == 0 and response_json['req_0']['code'] == 0:
                ext = '.m4a'
                download_url = str(response_json["req"]["data"]["freeflowsip"][0]) + str(response_json["req_0"]["data"]["midurlinfo"][0]["purl"])
                filesize = item['size128']

        if (not download_url) or (filesize == '-MB') or (filesize == 0): continue
        filesize = str(round(filesize/1024/1024, 2)) + 'MB'
        duration = int(item.get('interval', 0))
        songinfo = {
                    'source': 'qq',
                    'songid': str(item['songmid']),
                    'singers': filterBadCharacter(','.join([s.get('name', '') for s in item.get('singer', [])])),
                    'album': filterBadCharacter(item.get('albumname', '-')),
                    'songname': filterBadCharacter(item.get('songname', '-')),
                    'savedir': "downloaded",
                    'savename': '_'.join(['qq', filterBadCharacter(item.get('songname', '-'))]),
                    'download_url': download_url,
                    'filesize': filesize,
                    'ext': ext,
                    'duration': seconds2hms(duration)
                }
        songinfos.append(songinfo)

    print(songinfos)
    return songinfos,session

def downloader(songinfo,session):
    is_success = False
    with closing(session.get(songinfo[0]['download_url'], headers=headers, stream=True, verify=False)) as response:
        total_size = int(response.headers['content-length'])
        chunk_size = 1024

        if response.status_code == 200:
            label = '[FileSize]: %0.2fMB' % (total_size/1024/1024)
            with click.progressbar(length=total_size, label=label) as progressbar:
                with open(os.path.join(os.path.split(os.path.realpath(__file__))[0] , songinfo[0]['savename']+songinfo[0]['ext']), "wb") as fp:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            fp.write(chunk)
                            progressbar.update(chunk_size)
    is_success = True



if __name__ == '__main__':
    keyword = '等你下课'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    songinfos,session = main(keyword)
    downloader(songinfos,session)
