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


if __name__ == '__main__':

    # url = "https://kst-api.ai.99.com/reg_exercise/"

    img_path = "111.jpg"
    user_id = "netdragontest"
    
    # insert data
    # data_add(img_path, user_id)

    # search data
    # data_search(user_id)
