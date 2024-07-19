import datetime
import os
import time
import urllib.request

import oss2
import win32con
import win32gui

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

    url = fr'https://xxx/{year}/{month}/{day}/{hour}{minute}00_0_0.png'

    file_path = fr'{os.getcwd()}\earth.png'
    download_png(url, file_path)
    if os.stat(file_path).st_size > 10 * 1000:
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
