# -*- coding: utf-8 -*-

import oss2
import os


endpoint = "oss-cn-hangzhou.aliyuncs.com"
accesskey_id = "xxx"
accesskey_secret = "xxx"
bucket_name = "xxx"
download_local_save_prefix = "/home/workspace/images/";

def prefix_all_list(bucket, prefix):
    print("such as: ", prefix)
    oss_file_size = 0
    for obj in oss2.ObjectIterator(bucket, prefix ='%s/'%prefix):
         print('key : ' + obj.key)
         oss_file_size = oss_file_size + 1
         download_to_local(bucket, obj.key, obj.key)

    print(prefix +" file size " + str(oss_file_size))


def root_directory_list(bucket):
    for obj in oss2.ObjectIterator(bucket, delimiter='/'):
        if obj.is_prefix():  # is dir
            print('directory: ' + obj.key)
            prefix_all_list(bucket, str(obj.key).strip("/")) #去除/
        else:  # is file
            print('file: ' + obj.key)
            download_to_local(bucket, str(obj.key) , str(obj.key))


def download_to_local(bucket, object_name, local_file):
    url = os.path.join(download_local_save_prefix, local_file)
    file_name = url[url.rindex("/")+1:]
    file_path_prefix = url.replace(file_name, "")
    if not os.path.exists(file_path_prefix):
        os.makedirs(file_path_prefix)
        print("directory don't not makedirs "+  file_path_prefix)

    bucket.get_object_to_file(object_name, url)


if __name__ == '__main__':
    print("start \n");
    auth = oss2.Auth(accesskey_id, accesskey_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name);
    # download simple dir
    #prefix_all_list(bucket, "newDown");
    root_directory_list(bucket);
    print("end \n");
