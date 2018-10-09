# coding=utf-8
import random
import requests
import base64
import os
# import httplib
# import http.client
import json
import urllib.request
import urllib.parse
import cv2

import requests
from PIL import Image
from io import BytesIO

# img_src = "http://img.my.csdn.net/uploads/201212/25/1356422284_1112.jpg"
# response = requests.get(img_src)
# image = Image.open(BytesIO(response.content))
# image.save('9.jpg')


# url = "http://192.168.46.111:9800/v1/face/recognition/"
# url = "http://recognition.image.myqcloud.com/ocr/handwriting"
url = "http://192.168.46.120:3600/v1/lottery/recognition/"
img_path = 'E:/workspace/dlt.bmp'
# img_path = 'E:/workspace/download/use_images/00004/0020.jpg'
# # IMG_DIR = 'E:/Face-detect-recog/test_image/'
# # img = cv2.imread(img_path)
# # cv2.imshow('show', img)
# # cv2.waitKey(0)

def face_recog():
    import urllib.request
    import urllib.parse
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())

    # headers = {
    #     'authorization': 'EffXbIese0gDkTMLNjZEMaOQeBZhPTEyNTcyMzIyNjYmaz1BS0lESFZhVUNqQUhHZnc1Mm1MamJIbDNFTVJzQUhDdnhud3UmZT0xNTMzNDQyNDgyLjg4JnQ9MTUzMzE4MzI4Mi44OCZyPTU2NjI5OTQ5MTUmdT0wJmY9'
    # }

    params = {
        # 'img_url': "http://img.my.csdn.net/uploads/201212/25/1356422284_1112.jpg",
        # 'img_str': img,
        # 'top_n': 8
        'img_str': img,
        # 'appid': "1257232266"
    }

    params = urllib.parse.urlencode(params).encode(encoding='utf-8')
    with open("test.txt", 'wb') as wf:
        wf.write(params)

    request = urllib.request.Request(url=url, data=params)

    response = urllib.request.urlopen(request)
    content = response.read().decode()
    if content:
        print(content)
        print(type(content))

face_recog()


# if __name__ == '__main__':

#     IMG_DIR = 'E:/Face-detect-recog/test_image_2/'
#     for file in os.listdir(IMG_DIR):
#         print(file)
#         if file.endswith('.jpg'):
#             file_path = os.path.join(IMG_DIR, file)
#             print(file_path)
#             face_recog(file_path)


# face_recog(img_path)


# str_bytes = "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"

# print(type(str_bytes))
# with open('jiaye.jpg', 'wb') as wf:
#     wf.write(base64.b64decode(str_bytes))



#### post json格式请求图片数据 法二
frame = cv2.imread(img_path)
ret, jpeg = cv2.imencode('.jpg', frame)
str_data = jpeg.tostring()

headers = {'Content-Type': 'application/json'}
params = "{\"img_str\":\"/9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCABaAPoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD0PwX4L8K3XgXw9cXHhrRpp5dMtnkkksImZ2MSkkkrkknnNbn/AAgng/8A6FTQ/wDwXQ//ABNHgT/knnhr/sFWv/opa6CgDn/+EE8H/wDQqaH/AOC6H/4mj/hBPB//AEKmh/8Aguh/+JroKKAOf/4QTwf/ANCpof8A4Lof/iaP+EE8H/8AQqaH/wCC6H/4mugooA5//hBPB/8A0Kmh/wDguh/+JpkngnwXCoaXwxoCKSAC1hCBk9B92ujrhfiZ+/i8L6cOftmv2quvqilnb/0EUAbX/CCeD/8AoVND/wDBdD/8TR/wgng//oVND/8ABdD/APE10FFAHP8A/CCeD/8AoVND/wDBdD/8TR/wgng//oVND/8ABdD/APE10FFAHP8A/CCeD/8AoVND/wDBdD/8TR/wgng//oVND/8ABdD/APE10FFAHP8A/CCeD/8AoVND/wDBdD/8TR/wgng//oVND/8ABdD/APE10FFAHP8A/CCeD/8AoVND/wDBdD/8TR/wgng//oVND/8ABdD/APE10FFAHP8A/CCeD/8AoVND/wDBdD/8TR/wgng//oVND/8ABdD/APE10FFAHP8A/CCeD/8AoVND/wDBdD/8TR/wgng//oVND/8ABdD/APE10FFAHP8A/CCeD/8AoVND/wDBdD/8TR/wgng//oVND/8ABdD/APE10FFAHP8A/CCeD/8AoVND/wDBdD/8TR/wgng//oVND/8ABdD/APE10FFAHP8A/CCeD/8AoVND/wDBdD/8TR/wgng//oVND/8ABdD/APE10FFAHP8A/CCeD/8AoVND/wDBdD/8TR/wgng//oVND/8ABdD/APE10FFAHP8A/CCeD/8AoVND/wDBdD/8TXx540ghtfHXiG3t4o4YItTuUjjjUKqKJWAAA4AA4xX3HXxB47/5KH4l/wCwrdf+jWoA+v8AwJ/yTzw1/wBgq1/9FLXQVz/gT/knnhr/ALBVr/6KWugoAKKKKACiiigArhfFZF18TvA1j1WN7y7cem2IKp/Nv0ruq8+8LRp4p8f6z4ukUPa2JOlaW3YhCTNIPXLEgH0BoA9BooooAKKKKACiiigAooooAKKKKACgkAZJxRXyN8VfE+vP411bTZNUvVtEkKC2LlVVeuCBwfr70AfSepfEPwhpMhjvfENikgOCiyb2H1C5Iqxo/jXwzr8gi0vXLG5mPSJZQJD/AMBOD+lfJXg74d6945S5k0hbfy7dgsjzS7cE8j1PapvE3wx8WeEITd39gTbJybm3feq/XHI/KgD7Nor5O8GfGzxF4aaO21CRtT04YHlyn50H+y3X8DX0x4Y8T6b4t0aLU9Mm3xPwyn7yN6EUAbNFFcHD8YvBT6hNYy6obaeGRo3E8TKAwODzjB5HagDvKKqWGq6fqlmLuwvYLm3JIEsUgZcjqMjv7U9760j+/dQL/vSAUAWKKjhnhuI/MglSVOm5GDD8xUlABXxB47/5KH4l/wCwrdf+jWr7fr4g8d/8lD8S/wDYVuv/AEa1AH1/4E/5J54a/wCwVa/+ilroK5/wJ/yTzw1/2CrX/wBFLXQUAR3EvkW0s3lvJ5aFtkYyzYGcAdzXjujfH+yjvGsPFui3ejXSNhnVGdV/3kIDr+ANezVmaz4c0XxDAsOsaZa3qL93zowxX6HqPwoAxLb4o+B7oAx+JtPXP/PV/L/9CArRTxt4UkQunifRmUDJIv4uB7/NVOf4beCrnO/wvpQz/wA87ZU/9BxUNl8LfA+n3ZuoPDViZCNv75TKo+iuSoPuBmgDJ1bxZP4zvX8NeCL1HBUf2jrMR3R2kZ/hjI+9IwzjHT9R0lmnh74e+F7OwkvoLHTrVSkb3cwUucljycZYkk4HrwK2LPT7LTo2jsrO3tkY5ZYIggJxjJAHoBXl/wC0Lp/2v4cx3QHNnfRyE+isGQ/qy0AdNpnxS8K6yNWbT715odLg8+ebyiiFeR8u7BPI9McivP8ARf2ire88RraajpQt9Nlk2R3CSEtHk4BYHgj1xXhnh/UJ4De6bFPFBHqsK2sssr7VjXzFbcT/AMBI+hNVtasLbTNVmtLPUodRhjI23MKkK30zQB9w3ms6bp9mLy8vYIbdgCJHcAEHpUeleINI1yMvpepW12oOMxSBq+Ptb8Yat4m0LSNJ8qUx6bbGJ2QlvN+bIZhjjAAH4H1rI0DUdTstShTTdUl06SR9vnRyMm3d8pORz0JoA+5priC3CmaaOIOwVd7Bck9AM96zbzxR4f07P23XdNtiOomu0U/qa8ns/wBnpbycXPibxTfahMeWEQwfpvcsT+QqTxj8O/h/4H8O/wBoHRPPkEirunupD9MjOCCdoPHAYntQB2GofGHwJp4w2vwzNzxbo8n6qCK5+7/aG8HwZEFvql0QSMxwKoI9fmYV84T62ZFVLSytrY4iUlIUJJRQM5Izljlm5wScdABXeeG/hNrHinTVvppZWhdiUl3cnkqRgjJOQOSQAFI6kYAOuP7Rl3I6xweGP3u4f6y7CrjJ4xs44I5z2zjtXQWXjL4r+IbZbjR/Cmj29s/SW4uQ+PwDg/pXlXxD+GF14SVbq3AeJiSyxjpluCFyxCjeiclue5zXRfBPx80GtDS9UnaRrh0htucZLhVOfXHlx4/3m9aAO7/sb4z6jzP4l0TTUPVbeHew/OM/zrwX4i6PqOjeJ5IdU1U6ldNu3zMhRshiDwexOSPUGvtGvmf9onTtniu01BCSptkhkz13bpGU/lkf8BoAr/AvRpNfuNYtE1/VtKMKRyAafMsfmAkg7sqemB+deySfDETxtHP428Yyo4wynUlAI9MBK8G+CvinTfCviu4udUvFtbaaDymdgSOuew9QK+hk+KXgh4zIviOyKgZ+8QfyxmgD5a+I/hWLwb42vdHtpJJLZAkkLSkFirKDyQBkg5H4V0PwU06017xVcaNf3N/HBJbNKgtbt4cupHXaeeCayfit4ntPFnju51CwJa1SNYY2P8QXPP5k1vfs/Wsk/wASlnUHZb2kjMfTOFH86AO/+J3hTRfBPhNdYtLS9vpBcpE6XWp3G0Kwbn5XHOQPzr5yupkuLyeaOIQpJIzrGGLbATkDJ5OPU81926ppWn61YvZanZw3dq5BaKZdykg5HFfJPxi8PWfhv4i3dpp9sltZSwxTQwoMKoK4OP8AgSsaAOi+E1v8Nrrw9djxgLBdRS6PltczOmYiq4xggH5t1eseH/CHwq8Rx3EmiaVp16lu4SVkDkKxGQMk8/hXzr4C8BXfj/ULuysr62tZreISkThsMucHGB2yPzr6Q+Ffw4uvh5a6ilzqkd6160bbI4iqxld3Qk853eg6UAdrpOj6doVgtjpdnFaWqksIohhQT1NXaKKACviDx3/yUPxL/wBhW6/9GtX2/XxB47/5KH4l/wCwrdf+jWoA+v8AwJ/yTzw1/wBgq1/9FLXQVz/gT/knnhr/ALBVr/6KWugoAKKjnSSS3lSGTypWQhHwDtOODg+leGn4WfEvxMc+JvGpt4X+9DDI7j8UXYn60Aet6v4w8OaDuGqa3YWrr1jedd//AHyOT+VcHq/7Qfg6w3LYrfak46GKHy0/Evg/oaj0j9nnwlZbX1Ge/wBSfuryeUh/BcH/AMervNI8EeF9B2nTNBsLd16SCENJ/wB9nLfrQB5R/wALb+IXibjwr4JaOJ+FnmR5R9d52IPxzWV4m8J/FvXfDGpXvibV4IrG3t3uJbBZVG8IN+Nsa7T93ueoFfRdV9QtVvtNurN/uzwvEc+jAj+tAHxF4QsbHVPGOj6fqQc2d1dxwShG2nDMF69uSK9A+OPgbR/B11ojaJZ/Zra5ilRx5jPudCpySxJzh/0ry6xuX07VLa6AIktplkx3BVgf6V9HftH2qz+C9Jvl58q+CAj+68bH/wBkFAGL+zfbWVzB4h8yFHuEMIO4ZyjB8fqD+deM65pyaR4ourJ8iCOf5SP+eZOR/wCOkV6h+zheGPxhqdmDgTWXmHPfa6j8/m/nXI/F+yFl8TtXRMeS7q8YHYFRkfgc0AfWHhq+m1Lw9aXc7K7yBsSIcrIoYhXHsygN+NebfHtCfDUe4GRC6uY2ztTYH+fgcffC56ZZPWul+D96l78NdLKSu6xJ5QRwN0YXjBx16ZHsRTvirosuseC7vyVLPChZsLk7e/vt6FgOw45AoA+RtHjtptXtYrsgQvKoYs21QMj7x7D1PbrX1Hb/ABK0jQdAhQHzHhG66MispRnOTv8ALVtrb3G4nA5JG7pXyfyrHqCK9P8ACnwj1HxXZxXLXEyxyKiiVdkixZRWBbLqwAVxwAxOCPlxmgDZ8Y/Fu08Q2r22YmQy7VeNSxjX5Tld0aHbkZGSSWUEhcCvKdF1BtM163vLZGZkc+WM4YEggEEdGGcgjuBX0lo/wF0TTIlEt291IxzK7xYJx0CYb5B+Z9xTda+BGjahEotJFtX24JVchBwcKO5JzyT+vNAHpHh7UW1XRYLppI5CcoXjOVZlO1iD3BYHBHBGCOteS/tG6cX8O6fqKIw23KwytjII2yFfyO7/AL6r1LwnpNzouhw2NyY90ShVSLOyNQMBR6kdyABz04rk/jdZif4eXdwgImiG0OQdqocFs+mdoAP94gd6APlTStNm1fVbXTrdkWW5kEas5wqk9yewHc12mq/BfxzpSeZ/ZP2uP+9aSCT/AMd+9+lcXpNy9nq9pcRyBGSVTuJwAM859sV9327pJbRPGCEZAVB6gYoA+IrfwV4mursWsWhX5lJwAYGA/PFfTnwk+HR8DaJLLe7W1W9wZyDkRqOiA/iSa9FooAK+cv2ldP8AL1zQtSA/19tJAT/uMGH/AKMNfRteMftIWYk8G6VeAZaG/wDL+gdGP80FAHmnwE1D7F8UbaDOBe200B/BfM/9p19ZV8T/AA5vDYfEjw7ODgfb4oyfZ22H9Gr7YoAKKKKACviDx3/yUPxL/wBhW6/9GtX2/XxB47/5KH4l/wCwrdf+jWoA+v8AwJ/yTzw1/wBgq1/9FLXQVz/gT/knnhr/ALBVr/6KWugoAKKKKACiiigAooooA+D9ciEOv6lEOiXUqj8HIr6R+Mf+lfBCznbkg2sn4lcf1roLL4M+Cre8nvLrTn1C5nlaVnu5SwBYkkBRhcc9wT7102u+FtI8R+HzoeoWxawwoWONymzb93BHpigD5p+AMhT4nxIDjzLSVT+QP9KPj5EI/ibM23DSW0TEjoeMf0r2Dwn8GLDwZ40i13TdVuJLdI5I/s1xGCw3DGd4x/6D+NV/HHwbPjjxmdYuNXFpaeSkflRxbnJGe5IA6+9AFn4DyvJ8NoQzyNsmdQHHT6HuP5DFelTwrcQPExIDDGVOCPce9Y3hLwpp3g3Qo9J0wzNArFy0rbmZj1PYVu0AfH/xU8GXPhfxFJMISbS4YsJUjCoWz0wOFPfHA9OOA7wh8VdT8KWoiVGuBHxEhKKo45ydhY/QMPfNfUXibwppvirT3tb6PDFSqyqBuA9Pp7V47c/s5mW7by9YjjiLZBW3PA9D83H0GfrQBy+ofHzxFfkRLaxQWwOcRTOsrH3kUjj2AFQ2Xxz8RW0rNMA6Ek+VGQmTn+JiCT+nvnt6lo/7P3hnTVElzdXV7dD+KVU8of8AbPB/Umtef4MeFLmMJLC6jqRAscYz6jC5H0zj2oA2Ph94vPjTwzHqbweTKG2Oqg7SfbP+JqD4qRCX4cawGIAWLdyARx6g/e+nritfwt4ZtPCmlf2bY5FqrFkUszFc9eSTVnX9Gi8QaHdaVPLJFFcpsd48blB67Seh96APhRDh1OAeRwelfduhSGbw/p0rNuL20bE/VRXLaZ8IPA+mRBV0SG4fGGe5YyFvfBOB+ArtoYY7eCOGFAkUahEVRwoAwAKAH0UUUAFcR8WtAk8RfDrUraFC88AFzEoHJKen4E129BAIIIyD2oA+CtOu207VLS9UfNbzJKB7qwP9K+t4vjH4JGiQ6hc61FG7IC1uFZpQ2Om0Anr36e9cH48+AUt/qs2peF5oo1nYvJaSnAVj12n09jWJon7OOuXMgbWdVtLKHPKwAzSH+QH5mgD6Ps7qO9soLuHPlTxrImRg4YZH86mqvY2iWGn21nGxZLeJYlLdSFAAz+VWKACviDx3/wAlD8S/9hW6/wDRrV9v18QeO/8AkofiX/sK3X/o1qAPr/wJ/wAk88Nf9gq1/wDRS10FfDkHjTxVa28Vvb+JdZhgiQJHHHfyqqKBgAANgADjFSf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/RXxB/wAJ34w/6GvXP/BjN/8AFUf8J34w/wChr1z/AMGM3/xVAH2/XxB47/5KH4l/7Ct1/wCjWo/4Tvxh/wBDXrn/AIMZv/iqw555rq4luLiWSaeVy8kkjFmdickknkknnNAH\"}"
# params = "{\"img_str\": \"/9j/4AAQSkZJRgABAgAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL\"}"
# params = "{ \
#     \"img_str\": \"str_data\" \
# }"
result = requests.post(url, data=params, headers=headers, timeout=10)
print(result)
print(result.text)




######### form-data格式请求图片数据
def ReadFileAsContent(filename):  
    #print filename  
    try:  
        with open(filename, 'rb') as f:  
            filecontent = f.read()  
    except Exception as e:  
        print('The Error Message in ReadFileAsContent(): ' + e.message)
        return ''  
    return filecontent


def random_string(num):
    import string
    rand_str = ''
    for _ in range(num):
        rand_str += ''.join(random.sample(string.ascii_letters + string.digits, 1))
        # print(rand_str)
    return rand_str


def post_multipart(host, selector, fields, files):  
    content_type, body = encode_multipart_formdata(fields, files)
    print(content_type)
    body_buf = bytearray(body)
    h = httplib.HTTP(host)  
    h.putrequest('POST', selector)  
    h.putheader('content-type', content_type)  
    h.putheader('content-length', str(len(body_buf)))  
    h.endheaders()  
    h.send(body_buf)  
    errcode, errmsg, headers = h.getreply()  
    print(errcode, errmsg)
    # print(h.file.read())
    # print(headers)
    return h.file.read()
  

def encode_multipart_formdata(fields, files):

    # LIMIT = '----------%s' % ''.join(random.sample('0123456789abcdef', 15))
    # LIMIT = '----------lImIt_of_THE_fIle_eW_$'
    LIMIT = "----" + random_string(20)
    # print(LIMIT)
    body = []
    for (key, value) in fields:
        body.extend(bytes('\r\n--' + LIMIT + '\r\n'))
        body.extend(bytes('Content-Disposition: form-data; name="%s"\r\n' % key))
        body.extend(bytes('\r\n'))
        body.extend(bytes(value))
    for (key, filename, value) in files:
        body.extend(bytes('\r\n--' + LIMIT + '\r\n'))
        body.extend(bytes('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename)))
        body.extend(bytes('Content-Type: %s\r\n' % get_content_type(filename)))
        body.extend(bytes('\r\n'))
        body.extend(value)
    body.extend('\r\n--' + LIMIT + '--\r\n')
    content_type = 'multipart/form-data; boundary=%s' % LIMIT
    return content_type, body  


def get_content_type(filename):
    import mimetypes  
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'  
  
  
if "__main__" == __name__:

    img_path = 'E:/Face-detect-recog/test_image/920223/920223_3.jpg'
    data = ReadFileAsContent(img_path)
    # data = [0x01, 0x02, 0x03, 0x04]
    fields = [("type", "0")]
    files = [("up_img", "920223_3.jpg", data)]
    response_str = post_multipart("127.0.0.1:9800", "/v1/face/recognition/", fields, files)
    print(response_str)









# def get_content_type(filename):  
#     import mimetypes  
#     print(mimetypes.guess_type(filename))
#     return mimetypes.guess_type(filename)[0] or 'application/octet-stream'  
  

# def isfiledata(p_str):   
#     import re  
#     r_c = re.compile("^f'(.*)'$")  
#     rert = r_c.search(str(p_str))  
#     #rert = re.search("^f'(.*)'$", p_str)  
#     if rert:  
#         return rert.group(1)  
#     else:  
#         return None  
      

# def encode_multipart_formdata(fields):  
#     ''''' 
#             该函数用于拼接multipart/form-data类型的http请求中body部分的内容 
#             返回拼接好的body内容及Content-Type的头定义 
#     '''  
#     import random  
#     import os  
#     BOUNDARY = '----------%s' % ''.join(random.sample('0123456789abcdef', 15))
#     print(BOUNDARY)
#     CRLF = '\r\n'  
#     L = []  
#     for (key, value) in fields:  
#         filepath = isfiledata(value)
#         print(filepath)
#         print(os.path.basename(filepath))
#         if filepath:  
#             L.append('--' + BOUNDARY)  
#             L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, os.path.basename(filepath)))  
#             L.append('Content-Type: %s' % get_content_type(filepath))  
#             L.append('')  
#             L.append(str(ReadFileAsContent(filepath)))   
#         else:  
#             L.append('--' + BOUNDARY)  
#             L.append('Content-Disposition: form-data; name="%s"' % key)  
#             L.append('')  
#             L.append(value)    
#     L.append('--' + BOUNDARY + '--')  
#     L.append('')
#     print(L)
#     body = CRLF.join(L)  
#     content_type = 'multipart/form-data; boundary=%s' % BOUNDARY  
#     return content_type, body


# form_data = [('gShopID','489'),("addItems", r"f'E:/Face-detect-recog/test_image/920223/920223_3.jpg'"), ('validateString', '92c99a2a36f47c6aa2f0019caa0591d2')]  

# form_data = [("up_img", "f'E:/Face-detect-recog/test_image/920223/920223_3.jpg'")]

# form_data_re = encode_multipart_formdata(form_data)  

# # print(form_data_re)

# response = requests.post(url, data=body, headers=content_type)
# print(response.text)
