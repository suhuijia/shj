# -*- encoding: utf-8 -*-
# @Author: SHJ
# @Time: 2024-11-04 5:59 下午
# -*- coding: utf-8 -*-
import os
import urllib.request
import urllib.error
import time
import json
import shutil
import traceback
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
key = "w-gtHk15qk1Sn93A7WZ6OAa0USnYbhzX"
secret = "KnEYqAdl_nQIopv6FQQsd644L2kxmcR3"


def request_data(filepath):
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    fr = open(filepath, 'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(fr.read())
    fr.close()
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('1')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    return data, boundary


image_root = "/Users/a58/workspace/dataset/aiInterview/FBS_CLASS_new3"
save_dir = "/Users/a58/workspace/dataset/aiInterview/FBS_CLASS_new3_face++/add_dataset"
os.makedirs(save_dir, exist_ok=True)
for file in os.listdir(image_root):
    if file.startswith('.'): continue
    filepath = os.path.join(image_root, file)
    json_file = os.path.join(save_dir, file.split('.')[0] + '.json')
    if os.path.exists(json_file): continue

    data, boundary = request_data(filepath)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        print(file)
        # post data to server
        resp = urllib.request.urlopen(req, timeout=5)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        result = json.loads(qrcont.decode('utf-8'))

        ## 保存json文件
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False)

        face_attr = result["faces"][0]
        beauty = face_attr["attributes"]["beauty"]
        male_score = beauty["male_score"]
        female_score = beauty["female_score"]

        save_filename = file.split(".")[0] + "_{}_{}.jpg".format(str(int(male_score)), str(int(female_score)))
        save_path = os.path.join(save_dir, save_filename)
        shutil.copyfile(filepath, save_path)
        time.sleep(1)

    except Exception as e:
        print(traceback.format_exc())