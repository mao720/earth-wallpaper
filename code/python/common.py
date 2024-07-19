import datetime
import os
import time
import urllib.request

import win32con
import win32gui


def set_background(path):
    win32gui.SystemParametersInfo(
        win32con.SPI_SETDESKWALLPAPER, path, win32con.SPIF_SENDWININICHANGE
    )


def download_png(image_url, image_path):
    urllib.request.urlretrieve(image_url, image_path)


def start():
    url = fr'https://xxx.oss-cn-hongkong.aliyuncs.com/earth.png'
    file_path = fr'{os.getcwd()}\earth.png'

    download_png(url, file_path)
    if os.stat(file_path).st_size > 10 * 1000:
        time_now = datetime.datetime.now()
        print(f'{time_now}：刷新图片')
        set_background(file_path)
    else:
        print(f'未获取到最新图片({os.stat(file_path).st_size})')


if __name__ == '__main__':
    while True:
        try:
            start()
        except Exception as e:
            print(e)
        time.sleep(10 * 60)
