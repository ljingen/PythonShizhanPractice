"""
七牛云的人脸识别功能的python实现方式,需要先去注册自己的 secret 和 access key用于上传文件到七牛云的
空间进行处理,人像识别是七牛云的一项收费服务，项目价格为 1.5元/千次 ，测试前先存2元避免意外
"""
# -*- encoding:utf-8 -*-
import os
import base64
import json
import requests

from qiniu import Auth, put_file, etag
import qiniu.config
from PIL import Image


# 文件上传
def upload(bucket_name, path, filename, q, bucket_url):
    """
    上传文件
    :param bucket_name: 上传的服务器存储空间名称，要上传的空间
    :param path: 本地文件地址
    :param filename:上传到七牛后保存的文件名
    :param q:构建鉴权对象
    :param url:bucket_url 要操作的空间的外链地址
    :return:
    """
    token = q.upload_token(bucket_name, filename, 3600)

    # 要上传的本地文件 localfile
    print('正在上传...')
    localfile = path

    reform, inform = put_file(token, filename, localfile)

    if reform != None:
        print('已经成功地将{}--->{}'.format(filename, bucket_name))
        print('正在处理您的图片...')
        url = bucket_url + '/' +filename
        localfile = localfile.split('/')[-1]
        return url
    else:
        print('这里出现了一个小错误,无法上传')


# 调用API
def apiget(unurl, enurl):
    """
    组合出来url并去请求人脸对别服务。
    <!-- 人脸一对一比对API-->
    http://xxx.xxx.glb.clouddn.com/xxx.jpg?face-analyze/verification/url/<urlSafeBase64URI>
    :param bucket_url: 我们的七牛云公共库的虚拟url
    :param url: 我们base64加密了的需要进行对比的对比的图片的url
    :return:  调用七牛api并得到返回的json数据
    """
    try:
        url = unurl+'?face-analyze/verification/url/' + enurl
        # 标准对比的图片地址，名称为001.jpg
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("网络发生故障，请重试...")


# base64 Encode
def base64encode(url):
    try:
        print('正在加密链接...')
        enurl = base64.urlsafe_b64encode(bytes(url, "utf-8"))  # 这个是对什么进行加密的？
        print("已经加密完成...")
        enurl = str(enurl)
        enurl = enurl.split("'")[1]
        return enurl
    except:
        print("这里出现了一个问题，请重试!")


# PIL图片压缩
def pilresize(per, path):
    im = Image.open(path)  # 打开图片
    imsize = im.size
    sizex = int(imsize[0] * per)
    sizey = int(imsize[1] * per)
    im = im.resize((sizex, sizey))

    fname = path.split('/')[-1:][0]  # 获取文件名称
    fname2 = fname.split('.')[0]+'_ceshi.'+fname.split('.')[1]
    path2 = path.replace(fname,fname2)
    im.save(path2, 'JPEG')
    print('图片压缩完成，输出成功,待对比的照片名称为 {}'.format(fname))

    print('{} ->>({},{})'.format(imsize, sizex, sizey))


def pilwork(path):
    try:
        size = os.path.getsize(path) # 返回这个文件的大小
        print('这个图片的尺寸是:%s' %size)
        size = float(size)
        kb = size/1024
        print('这个图片的大小用Kb表示是:%d k' %kb)

        per = 10/kb
        print('这个图片得到的per值是:%f' %per)

        pilresize(per, path)
    except:
        print('请检查您的地址是否输入错误')

# json分析
def jsonanal(jtext):
    """
    主要是对返回的json结果进行一个个读取
    :param jtext:
    :return:
    """
    print("正在分析,请稍后...")
    rj = json.loads(jtext)
    stat = rj['status']  # 从里面取出来status字段
    confi = rj['confidence']  #从返回的jsong里面取出来相似度指数
    return stat+','+str(confi)


# 主函数
def main():

    # 填写你的AK和你的SK
    # access_key = input('请输入您在七牛云的AccessKey:')
    access_key = 'fJHMG0_3iXFfoLyKTAevDUheUxZP8dqmfuied63T'
    # secret_key = input('请输入您在七牛云的SecretKey:')
    secret_key = 'tGqeZmBW9KR-0Sfzxo7E5Kfa_NcMB7PXn1DAv_sU'

    # 鉴定身份
    q = Auth(access_key, secret_key)

    # 要操作的空间
    # bucket_name = input('请输入要操作的空间(公开)名称:')
    bucket_name = 'bucket01'

    # 要操作的空间的外链地址
    # bucket_url = input('请输入空间绑定的域名或者默认的外链地址:')
    bucket_url = 'http://p0ydhmq3c.bkt.clouddn.com'

    # 判断操作类型
    while 1:
        order = input('请输入您需要进行的操作:')
        mode = order.split(' ')[0]

        if mode == '识别':
            path = order.split(' ')[1]  # 获取路径
            fname = path.split('/')[-1:][0]  # 获取文件名称
            unurl = bucket_url + '/timg.jpg'  # 杨幂的真实的脸部照片，这个是要作为对比的地址
            # http://p0ydhmq3c.bkt.clouddn.com/timg.jpg  要对比的照片

            print('正在压缩图片...')
            pilwork(path)  # 使用pillow库压缩图片

            fname2 = fname.split('.')[0] + '_ceshi.' + fname.split('.')[1]  # 拼装成接下来在服务器保存的文件名字。
            path = path.replace(fname, fname2)

            print('正在上传token,请稍后...')
            url = upload(bucket_name, path, fname2, q, bucket_url)  # 上传文件

            enurl = base64encode(url)  # base64加密

            jtext = apiget(unurl, enurl) # 调用七牛api并得到返回的json数据

            result = jsonanal(jtext)  # 分析返回的json，得到相似度数据

            if result.split(',')[0] == 'invalid':
                print('识别发生了错误!')
            else:
                if eval(result.split(',')[1])>=0.7:
                    print('识别结束:鉴定为本人，相似度为{:.1f}'.format(eval(result.split(',')[1])*100))
                else:
                    print('识别结束,鉴定不是本人，相似度"%.2f%%' %(eval(result.split(',')[1])*100))

        if mode == '退出':
            print('欢迎您的使用...')
            break

print("+----------------------------------------+")
print("|        欢迎使用七牛的人脸识别功能      |")
print("+----------------------------------------+")
print("|1.本程序测试图片为杨幂的人像,见face.jpg |")
print("|2.您需要提供服务的Accesskey，Secretkey  |")
print("|3.您需要提供 bucket名字和bucket外链地址 |")
print("+----------------------------------------+")
print("|使用方法:                               |")
print("|1.识别输入格式： 识别 图片位置(包括后缀)|")
print("|2.退出输入格式： 退出                   |")
print("+----------------------------------------+")
main()
