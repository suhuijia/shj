# -*- coding: utf-8 -*-
import os
import json
import pandas as pd
import xlrd
import urllib.request
import requests
from tqdm import tqdm
from PIL import Image
from io import BytesIO
import wget
import zipfile
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def get_url_txt(URL):
    req = urllib.request.Request(URL)
    res = urllib.request.urlopen(req)
    get_txt = res.read().decode('utf-8')
    data = json.loads(get_txt)
    return data


def get_url_image(URL):
    response = requests.get(URL)
    image = Image.open(BytesIO(response.content))
    return image


def write_viewdata(viewdata_json, save_path):
    with open(save_path, 'w', encoding='utf-8') as wf:
        json.dump(viewdata_json, wf, ensure_ascii=False)


def readXml(xml_file, save_dir):
    """ 保存10套测试数据 """
    readbook = xlrd.open_workbook(xml_file)
    table = readbook.sheets()[1]
    nrows = table.nrows
    ncols = table.ncols
    print(table)
    for i in range(1, nrows, 3):
        zxidx = i
        fyidx = i + 2
        idx = int(table.row_values(zxidx)[0])
        print("idx: ", idx)
        case = 2
        if case == 1:
            ## 装修
            pano_id = int(table.row_values(zxidx)[2])
            viewdata_url = table.row_values(zxidx)[3]
        elif case == 2:
            ## 房源AR
            pano_id = int(table.row_values(fyidx)[2])
            viewdata_url = table.row_values(fyidx)[3]

        viewdata = get_url_txt(viewdata_url)
        ImageUrl = viewdata['HouseData']['Floors'][0]['Plan']['ImageUrl']
        image = get_url_image(ImageUrl)

        save_dirs = os.path.join(save_dir, str(idx))
        os.makedirs(save_dirs, exist_ok=True)

        save_dirs_pano = os.path.join(save_dirs, str(pano_id))
        os.makedirs(save_dirs_pano, exist_ok=True)

        viewdata_file = os.path.join(save_dirs_pano, "ViewData.txt")
        image_file = os.path.join(save_dirs_pano, "base_export.png")
        write_viewdata(viewdata, viewdata_file)
        image.save(image_file)


def readXml1000(xml_file, save_dir):
    """ 保存1000套测试数据 """
    save_zipdir = os.path.join(save_dir, 'pano_zipfile')
    save_unzipdir = os.path.join(save_dir, 'pano_extract')
    os.makedirs(save_zipdir, exist_ok=True)
    os.makedirs(save_unzipdir, exist_ok=True)
    readbook = xlrd.open_workbook(xml_file)
    table = readbook.sheets()[2]
    nrows = table.nrows
    ncols = table.ncols
    print(table)
    for i in range(1, nrows):
        pano_id = str(int(table.row_values(i)[0]))
        pano_url = table.row_values(i)[2]
        save_zipfile = os.path.join(save_zipdir, pano_id + '.zip')
        # filename2 = wget.download(pano_url, out=save_zipfile)
        if not os.path.exists(save_zipfile):
            download(url=pano_url, fname=save_zipfile)
        save_unzipfile = os.path.join(save_unzipdir, pano_id)
        unzip_file(save_zipfile, dst_dir=save_unzipfile)


def download(url: str, fname: str):
    res = requests.get(url, stream=True)
    total = int(res.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in res.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def unzip_file(zip_src, dst_dir):
    """ 解压zip文件 """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print("zip file is wrong.")


def readTxt(txt_file, save_dir):
    """ 保存10套测试数据 """
    with open(txt_file, 'r', encoding='utf-8') as rf:
        data = rf.readlines()

    for line in data:
        line = line.strip()
        pano_id = os.path.basename(line)
        print("pano_id: ", pano_id)
        viewdata = get_url_txt(line)
        ImageUrl = viewdata['HouseData']['Floors'][0]['Plan']['ImageUrl']
        print("ImageUrl: ", ImageUrl)
        image = get_url_image(ImageUrl)

        save_dir_pano = os.path.join(save_dir, pano_id)
        os.makedirs(save_dir_pano, exist_ok=True)

        viewdata_file = os.path.join(save_dir_pano, "ViewData.txt")
        image_file = os.path.join(save_dir_pano, "base_export.png")
        write_viewdata(viewdata, viewdata_file)
        image.save(image_file)


def readTxtAuto(txt_file, save_dir):
    """ 下载自动拼接的viewdata 暂不使用"""
    viewdata_url_pre = 'http://quanjing.a.ajkdns.com/data/standard-viewdata/'

    with open(txt_file, 'r', encoding='utf-8') as rf:
        data = rf.readlines()

    for line in data:
        pano_id = line.strip()
        print("pano_id: ", pano_id)
        viewdata_url = viewdata_url_pre + pano_id
        viewdata = get_url_txt(viewdata_url)
        ImageUrl = viewdata['HouseData']['Floors'][0]['Plan']['ImageUrl']
        print("ImageUrl: ", ImageUrl)
        image = get_url_image(ImageUrl)

        save_dir_pano = os.path.join(save_dir, pano_id)
        os.makedirs(save_dir_pano, exist_ok=True)

        viewdata_file = os.path.join(save_dir_pano, "ViewData.txt")
        image_file = os.path.join(save_dir_pano, "base_export.png")
        write_viewdata(viewdata, viewdata_file)
        image.save(image_file)


def readJsonAuto(json_file, save_dir):
    """ 下载自动拼接viewdata """
    save_zipdir = os.path.join(save_dir, 'pano_zipfile')
    save_unzipdir = os.path.join(save_dir, 'pano_extract')
    os.makedirs(save_zipdir, exist_ok=True)
    os.makedirs(save_unzipdir, exist_ok=True)

    with open(json_file, 'r', encoding='utf-8') as rf:
        data = json.load(rf)

    for i in range(100):
        ele = data[i]
        pano_id = ele["panoId"]
        resultpackage_url = ele["url"]
        save_zipfile = os.path.join(save_zipdir, pano_id + '.zip')
        if not os.path.exists(save_zipfile):
            download(url=resultpackage_url, fname=save_zipfile)
        save_unzipfile = os.path.join(save_unzipdir, pano_id)
        unzip_file(save_zipfile, dst_dir=save_unzipfile)


def extract_viewdata_image(root, save_dir):
    """ 提取viewdata和图像数据 """
    import shutil
    import glob
    os.makedirs(save_dir, exist_ok=True)
    for dir in os.listdir(root):
        save_dir_path = os.path.join(save_dir, dir)
        os.makedirs(save_dir_path, exist_ok=True)

        viewdata_file = os.path.join(root, dir, "ViewData.txt")
        images_files = os.path.join(root, dir, "./FloorPlans/*_base_export.png")
        image_file = list(glob.glob(images_files))[0]

        shutil.copy(viewdata_file, save_dir_path)
        shutil.copy(image_file, save_dir_path)


if __name__ == '__main__':

    # xml_file = "/Users/a58/workspace/vectorgraph/houselayout/pano_ULR.xlsx"
    # xml_file = "./pano_ULR.xlsx"

    ## 10套测试数据
    # save_viewdata_dir = "/Users/a58/workspace/vectorgraph/houselayout/test_10"
    # readXml(xml_file=xml_file, save_dir=save_viewdata_dir)


    ## 1000套测试数据
    # save_viewdata_dir = "../test_1000"
    # readXml1000(xml_file=xml_file, save_dir=save_viewdata_dir)


    ## 解压文件
    # zip_src = "/Users/a58/workspace/vectorgraph/houselayout/test_1000/71986612.zip"
    # dst_dir = "/Users/a58/workspace/vectorgraph/houselayout/test_1000/71986612"
    # unzip_file(zip_src=zip_src, dst_dir=dst_dir)


    ## 解压文件夹
    # zipfile_dir = os.path.join(save_viewdata_dir, 'pano_zipfile')
    # for file in os.listdir(zipfile_dir):
    #     zipfile = os.path.join(zipfile_dir, file)
    #     save_unzipfile = os.path.join(save_viewdata_dir, 'pano_extract', file[:-4])
    #     unzip_file(zip_src=zipfile, dst_dir=save_unzipfile)


    # ## 读取txt文件
    # txt_file = "/Users/a58/workspace/vectorgraph/houselayout/t_decorate_task_1658984585.txt"
    # save_dir = "/Users/a58/workspace/vectorgraph/houselayout/test_1000_haifang"
    # readTxt(txt_file, save_dir)


    # ## 读取txt文件 获取 auto splicing viewdata
    # txt_file = "/Users/a58/workspace/vectorgraph/houselayout/auto_id.txt"
    # save_dir = "/Users/a58/workspace/vectorgraph/houselayout/test_100_auto"
    # readTxtAuto(txt_file, save_dir)


    ## 读取json文件，下载结果包
    json_file = "/Users/a58/workspace/vectorgraph/houselayout/auto_viewdatas.json"
    save_dir = "/Users/a58/workspace/vectorgraph/houselayout/houseLabels_100_auto_debug"
    readJsonAuto(json_file=json_file, save_dir=save_dir)


    # ## 从解压素材中提取viewdata和图像数据
    # root = "/code/shj/deep_learning/viewdata2houseLabel/panos/test_100_auto_json/pano_extract"
    # save_dir = "/code/shj/deep_learning/viewdata2houseLabel/panos/test_100_auto_json/pano_viewdataImage"
    # extract_viewdata_image(root, save_dir)
