# -*- coding: UTF-8 -*-

def data_add(img_path, user_id):
    import requests
    import json

    url = "https://kst-api.ai.99.com/reg_exercise/"
    headers = {
        'x-api-key': 'G2D2S1gaJM8ARXU50dFJigG33kGePps4SzdT3A70'  # my test key for aws api gateway
    }

    with open(img_path, 'rb') as fp:
        data = fp.read()

    data = {"need_img": "True",
             "user_id": user_id,
             "uuid": "nd",
             "user_info": "root_nd",
            }

    files = {"upl_img": open(img_path, 'rb'),}

    # files = json.dumps(files)
    r = requests.post(url=url, data=data, files=files, headers=headers, verify=False)
    # CaseInsensitiveDict({'Content-Length': '190914', 'Content-Type': 'multipart/form-data; boundary=7e4d21a7d6f0499fb73c0b618081177a', 'Accept-Encoding': 'gzip, deflate, compress', 'Accept': '*/*', 'User-Agent': 'python-requests/2.2.1 CPython/2.7.6 Linux/3.13.0-24-generic'})
    result = r.content
    if result:
        print(result)
        print(200, 'OK')
    else:
        print("FAIL.")


def data_search(user_id):
    import urllib.request
    import urllib.parse
    # import urllib2
    # import urllib

    url = "https://kst-api.ai.99.com/exercise_download"
    params = {
        "user_id": user_id,
    }
    params = urllib.parse.urlencode(params)
    url = '%s%s%s' % (url, '?', params)
    request = urllib.request.Request(url=url)
    response = urllib.request.urlopen(request)
    content = response.read().decode()
    if content:
        print(content)
        print(200, 'OK')
    else:
        print("NO DATA.")

def post36():
    # python3.x
    import urllib.parse
    import urllib.request
    import json
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=vWjMjyPllXDpgxAFDinRj4E7&client_secret=jU0KGMZUVGujYR7vS2YP5EWIOqXLbaHe'
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read().decode(encoding='utf-8')
    if (content):
        pass
    result=json.loads(content)
    expries_in=result["expires_in"]
    access_token=result["access_token"]
    url = "https://aip.baidubce.com/rest/2.0/face/v3/faceverify?access_token=" + access_token

    import base64
    f = open("sy.jpg", 'rb')
    img = base64.b64encode(f.read()).decode(encoding='utf-8')

    # params = "[{\"image\":\"http://kousuanti.oss-cn-hangzhou.aliyuncs.com/2019_07_09_221537_sy.jpg\",\"image_type\":\"URL\"}]"
    params = {"image":img, "image_type":"BASE64"}
    params = json.dumps(params)
    params = "[" + params + "]"

    # params = urllib.parse.urlencode(params).encode(encoding='utf-8')    # encode 将字符串编码为字节； decode将字节解码为字符串；
    params = params.encode()
    request = urllib.request.Request(url=url, data=params)                # post data 必须为字节，不能是字符串
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read()
    if content:
        print(content)


def post27():
    # python2.x  不严格区分字节和字符串，所以不需要很多的转换操作
    import urllib
    import urllib2
    import json
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=vWjMjyPllXDpgxAFDinRj4E7&client_secret=jU0KGMZUVGujYR7vS2YP5EWIOqXLbaHe'
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        pass
    result=json.loads(content)
    expries_in=result["expires_in"]
    access_token=result["access_token"]
    url = "https://aip.baidubce.com/rest/2.0/face/v3/faceverify?access_token=" + access_token

    import base64
    f = open("sy.jpg", 'rb')
    img = base64.b64encode(f.read())

    # params = "[{\"image\":\"http://kousuanti.oss-cn-hangzhou.aliyuncs.com/2019_07_09_221537_sy.jpg\",\"image_type\":\"URL\"}]"
    params = {"image":img, "image_type":"BASE64"}
    params = json.dumps(params)
    params = "[" + params + "]"

    # params = urllib.parse.urlencode(params).encode(encoding='utf-8')    # encode 将字符串编码为字节； decode将字节解码为字符串；
    # params = params.encode()
    request = urllib2.Request(url=url, data=params)                       # post data 必须为字节，不能是字符串
    request.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(request)
    content = response.read()
    if content:
        print(content)

if __name__ == '__main__':

    # url = "https://kst-api.ai.99.com/reg_exercise/"

    img_path = "111.jpg"
    user_id = "netdragontest"
    
    # insert data
    # data_add(img_path, user_id)

    # search data
    # data_search(user_id)
