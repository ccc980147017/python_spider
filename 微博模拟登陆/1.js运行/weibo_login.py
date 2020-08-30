import execjs,requests,time

username = ''  #微博账号
password = ''  #微博密码

ua = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': ua
}

session = requests.session()

def get_data(su):
    pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
    pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
    pre_url = pre_url + str(int(time.time() * 1000))
    pre_data_res = session.get(pre_url, headers=headers)
    sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))
    return sever_data

def get_su():
    node = execjs.get()
    file = 'weibo.js'
    ctx = node.compile(open(file, encoding='utf-8').read())

    js_su = "get_su('{}')".format(username)
    su = ctx.eval(js_su)
    return su

def get_sp(servertime, nonce, pubkey):
    node = execjs.get()
    file = 'weibo.js'
    ctx = node.compile(open(file, encoding='utf-8').read())

    js_sp = "get_sp('{}')".format(password, servertime, nonce, pubkey)
    sp = ctx.eval(js_sp)
    return sp

def main():
    su = get_su()
    sever_data = get_data(su)
    # print(sever_data)

    servertime = sever_data["servertime"]
    nonce = sever_data['nonce']
    rsakv = sever_data["rsakv"]
    pubkey = sever_data["pubkey"]
    showpin = sever_data["showpin"]

    sp = get_sp(servertime, nonce, pubkey)
    print(sp)



if __name__ == '__main__':
    main()
