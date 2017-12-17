# -*- encoding:utf-8 -*-
# flake8:noqa
__author__ = 'Amos'
__date__ = '2017/12/14 20:45'

import json
import os
import requests
import base64

from PIL import Image
from qiniu import Auth, put_file, etag, BucketManager
import qiniu.config

import faceverification
# 七牛云"人脸识别"功能的python实现方法：by xlxw
# 请得到自己的Secret和Access key用于上传图片到空间中进行处理
# 人像识别是七牛云的一项收费项目，价格为 ￥1.5/1000次 测试时请先存2元避免意外


# 上传文件
def upload(bucket_name, localfile, filename, q, url):
    '''
    :param bucket_name: 七牛上面的上传存储库
    :param localfile: 要上传文件的本地路径
    :param filename: 上传到七牛后保存的文件名
    :param q: 操作者当前身份验证的授权对象
    :param url:
    :return:
    '''
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, filename, 3600)

    print('正在进行上传文件')

    reform, inform = put_file(token, filename, localfile)

    if reform is not None:
        print('已经成功的将{}->>{}'.format(filename, bucket_name))
        print('正在处理您的图片...')
        url = url+'/'+filename
        path = localfile.split('/')[-1]
    else:
        print('这里出现了一个小错误，无法上传...')


# 调用API
def apiget(urlbucket, url):
    try:
        url= urlbucket+'/001.jpg'+'?face-analyze/verification/url/'+url
        # 标准对比的图片地址，名称为001.jpg
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("网络发生故障,请重试...")


def download(url, path):
    '''
    从七牛云下载文件
    :param url: 要下载的文件的url
    :param path: 存放文件的path
    :return:
    '''
    r = requests.get(url)
    contenter = r.content
    with open(path, 'wb') as filer:
        filer.write(contenter)
        filer.close()
    print('已经保存文件到{}'.format(path))


def delete(bucketer, filename, q):
    print('正在删除...')
    bucket = BucketManager(q)
    reform, info = bucket.delete(bucketer, filename)
    if reform is not None:
        print(info)
        print('已经成功的将{}-->>x'.format(filename))
    else:
        print('这里出现了一个小错误.(可能是存储空间没有这个文件)')

if __name__ == '__main__':

    faceverification.test()
    # 填写你的 AK 和你的SK
    # access_key = input('请输入你的七牛云的Accesskey:')
    access_key = 'fJHMG0_3iXFfoLyKTAevDUheUxZP8dqmfuied63T'

    # secret_key = input('请输入你的七牛云的Secretkey:')
    secret_key = 'tGqeZmBW9KR-0Sfzxo7E5Kfa_NcMB7PXn1DAv_sU'
    # 鉴定身份
    q = Auth(access_key, secret_key)

    # 所要操作的空间
    # bucket_name = input('请输入要操作的七牛云空间名称:')
    bucket_name = 'bucket01'

    # 判断操作的类型
    while 1:
        order = input('请输入你需要进行的操作:')
        mode = order.split(' ')[0]

        if mode == '上传':
            path = order.split(' ')[1]
            # 我知道为什么了加上[0]，如果刚好是/test.png  假设这个时候不加上 [0]  那么这个fname就是一个list
            # 不是一个具体的数值
            fname = path.split('/')[-1:][0]
            print('正在尝试生成Token,请稍后...')
            upload(bucket_name, path, fname, q)

        elif mode == '下载':
            print('正在尝试生成Token.请稍后..')
            download(order.split(' ')[1], order.split(' ')[2])

        elif mode == '更换':
            if order.split(' ')[1] == '空间':
                bucket_name = input('请输入您想要更改的空间(公开)名称:')
            elif order.split(' ')[1] == 'AK':
                access_key = input('请输入新的AK')
            elif order.split(' ')[1] == 'SK':
                secret_key = input('请输入新的SK')
            else:
                print('您输入的命令有误.')
        elif mode == '删除':
            print('正在尝试生成Token.请稍后..')
            delete(bucket_name, order.split(' ')[1], q)

        elif mode == '退出':
            break
        else:
            print('输入的命令有误，请重试!')
print('+----------------------------------------------------+')
print('|欢迎使用本Qiniu云的上传下载程序，以下为使用方法介绍: |')
print('+----------------------------------------------------+')
print('|1.请先输入您的Accesskey和secretKey进行鉴权           |')
print('|2.之后输入您要进行操作的bucket空间                   |')
print('|3.上传操作的命令为:  上传 文件地址(带后缀)           |')
print('|4.下载操作的命令为:  下载 链接地址 本地路径带后缀     |')
print('|5.删除操作的命令为:  删除 空间中的文件名称            |')
print('|6.更换bucket操作为:  更换 空间名                     |')
print('|7.更换AKSK的操作为:  更换 AK/SK                      |')
print('|8.退出程序的命令为:  退出     |')
print('+----------------------------------------------------+')
