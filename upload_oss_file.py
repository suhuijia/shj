import oss2
import time


def upload_ali_oss(path):
    filename = time.strftime('%Y_%m_%d_%H%M%S_', time.localtime(time.time())) + path.split('/')[-1]
    try:
        auth = oss2.Auth('xxx', 'xxx')
        bucket = oss2.Bucket(auth, 'oss-cn-hangzhou.aliyuncs.com', 'xxx')
        bucket.put_object_from_file(filename, path)
        return 'http://xxx.oss-cn-hangzhou.aliyuncs.com/' + filename
    except Exception as e:
        return None


if __name__ == '__main__':
    path = 'xxx/xxx/xxx.jpg'
    url = upload_ali_oss(path)
