import datetime
import os
import time
import urllib.request

import numpy
import oss2
import win32con
import win32gui
from PIL import Image

bucket = oss2.Bucket


def init():
    # 填写RAM用户的访问密钥（AccessKey ID和AccessKey Secret）。
    accessKeyId = 'xxx'
    accessKeySecret = 'xxx'
    # 使用代码嵌入的RAM用户的访问密钥配置访问凭证。
    auth = oss2.Auth(accessKeyId, accessKeySecret)
    global bucket
    bucket = oss2.Bucket(auth, 'https://oss-cn-hongkong.aliyuncs.com', 'xxx')


def set_background(path):
    win32gui.SystemParametersInfo(
        win32con.SPI_SETDESKWALLPAPER, path, win32con.SPIF_SENDWININICHANGE
    )


def download_png(image_url, image_path):
    urllib.request.urlretrieve(image_url, image_path)


def upload_oss(image_path):
    bucket.put_object_from_file('earth.png', image_path)


def start():
    time_now = datetime.datetime.utcnow() - datetime.timedelta(minutes=20)

    year = time_now.year
    month = f'{time_now.month}' if time_now.month >= 10 else f'0{time_now.month}'
    day = f'{time_now.day}' if time_now.day >= 10 else f'0{time_now.day}'
    hour = f'{time_now.hour}' if time_now.hour >= 10 else f'0{time_now.hour}'
    minute = time_now.minute // 10 * 10
    minute = f'{minute}' if minute >= 10 else f'0{minute}'

    url_0_0 = fr'https://xxx/2d/550/{year}/{month}/{day}/{hour}{minute}00_0_0.png'
    url_1_0 = fr'https://xxx/2d/550/{year}/{month}/{day}/{hour}{minute}00_1_0.png'
    url_0_1 = fr'https://xxx/2d/550/{year}/{month}/{day}/{hour}{minute}00_0_1.png'
    url_1_1 = fr'https://xxx/2d/550/{year}/{month}/{day}/{hour}{minute}00_1_1.png'
    file_path_0_0 = fr'{os.getcwd()}\earth_0_0.png'
    file_path_1_0 = fr'{os.getcwd()}\earth_1_0.png'
    file_path_0_1 = fr'{os.getcwd()}\earth_0_1.png'
    file_path_1_1 = fr'{os.getcwd()}\earth_1_1.png'
    download_png(url_0_0, file_path_0_0)
    download_png(url_1_0, file_path_1_0)
    download_png(url_0_1, file_path_0_1)
    download_png(url_1_1, file_path_1_1)

    image_0_0 = numpy.array(Image.open(file_path_0_0).convert(mode='RGB'))
    image_1_0 = numpy.array(Image.open(file_path_1_0).convert(mode='RGB'))
    image_0_1 = numpy.array(Image.open(file_path_0_1).convert(mode='RGB'))
    image_1_1 = numpy.array(Image.open(file_path_1_1).convert(mode='RGB'))

    row_0 = numpy.concatenate([image_0_0, image_1_0], axis=1)
    row_1 = numpy.concatenate([image_0_1, image_1_1], axis=1)
    image = Image.fromarray(numpy.concatenate([row_0, row_1], axis=0))
    file_path = fr'{os.getcwd()}\earth.png'
    image.save(file_path)

    if os.stat(file_path).st_size > 40 * 1000:
        print(f'New image：{year}-{month}-{day} {hour}:{minute} UTC')
        set_background(file_path)
        upload_oss(file_path)
    else:
        print(f'No image({os.stat(file_path).st_size})')


if __name__ == '__main__':
    init()
    while True:
        try:
            start()
        except Exception as e:
            print(e)
        time.sleep(10 * 60)
