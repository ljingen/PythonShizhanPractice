# -*- encoding:utf-8 -*-

import requests
import urllib
import re
import random
from time import sleep


def main():
    url = 'https://www.zhihu.com/'
    cookies = 'q_c1=d77b5fc6845045e3aaf9dfeee9dedeb0|1514512476000|1514512476000; _zap=a642c4fc-3ca6-43cf-acb2-4072f0eb' \
              'b' \
              '422; aliyungf_tc=AQAAAOwDywTiwgIAu1shcwMQlAobexdU; d_c0="ADBhstF16QyPTlO1jOxjT_Z9umY_QOFfgZI=|15146056' \
              '81"; _xsrf=d7e6eb3c-3169-4f7a-a438-429716bc1bf9; capsion_ticket="2|1:0|10:1514605684|14:capsion_ticket' \
              '|44:MDc2MTJjMGJmYjdiNDRmYTkyMDNmMDllMTE4YTEwMzM=|fa60f0853a50705b834029d5c2e4f91cc659dc885f8b8dbe1672af3' \
              '601adf6e2"; z_c0="2|1:0|10:1514605686|4:z_c0|92:Mi4xYVYwbkFBQUFBQUFBTUdHeTBYWHBEQ1lBQUFCZ0FsVk5kbG8wV3d' \
              'CUHZpVnVTV2prWnJCOUliZFQzUFlxV1VyVHl3|4c894aace83f3294a869bf16ceec8f2b86a7d809011ed08c0156e0772a7e8e17"'
    headers = {'content-type': 'text/html', 'charset': 'utf-8'}
    i = 925
    for x in range(1020, 2000, 20):
        data = {'start': '1000',
            'offset' : str(x),
            '_xsrf' : 'a128464ef225a69348cef94c38f4e428'}
        content = requests.post(url, headers=headers, data=data, timeout=10).text
        imgs = re.findall('<img src=\\\\\"(.*?)_m.jpg',content)

        for img in imgs:
            try:
                img =img.replace('\\','')
                pic = img +'.jpg'
                path= 'd:\\bs4\\zhihu\\jpg4\\'+str(i)+'.jpg'
                urllib.urlretrieve(pic, path)
                print('下载了第'+str(i) + u'张图片')
                i += 1
                sleep(random.uniform(0.5, 1))  # random.uniform(0.5,1) 生成一个随机的小数
            except:
                print('抓漏1张')
                pass
        sleep(random.uniform(0.5, 1))

if __name__ == '__main__':
    main()
