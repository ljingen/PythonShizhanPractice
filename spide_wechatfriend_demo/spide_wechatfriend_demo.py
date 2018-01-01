# -*- encoding:utf-8 -*-

import itchat


def fetch_friends_list():
    """
    爬取自己好友相关信息
    fetch friends list 获取好友列表
    for options
        - update: if not set, local value will be returned
    for results
        - a list of friends' info dicts will be returned
    it is defined in components/contact.py
    """
    itchat.login()
    friends = itchat.get_friends(update=True)[0:]
    return friends


def count_friens_sex(friends):
    """
    根据用户的好友列表，获取到这个用户的 男好友、女好友的百分比，以及用户的好友总数
    :param friends:
    :return:
    """
    # 初始化计数器
    male = female = other = 0

    # friends[0]是自己的信息，所以我们从friends[1:]开始,这个意思 是 从1开始到最后

    for mFriend in friends[1:]:
        # print("这个类型是:{}".format(type(mFriend))+"值是:{}".format(mFriend))
        sex = mFriend['Sex']
        if sex == 1:
            male += 1
        elif sex == 2:
            female += 1
        else:
            other += 1

    # 计算出来朋友总数量
    friend_total = len(friends[1:])

    # 打印出来自己的好友性别比例：
    print("好友总数是:%d" % friend_total + "\n" +
          "男性好友:%.2f%%" % (float(male)/friend_total*100) + "\n" +
          "女性朋友:%.2f%%" % (float(female)/friend_total*100) + "\n" +
          "不明性别好友:%.2f%%" % (float(other)/friend_total*100)
          )


def get_friend_value(friends, var):
    """
    获取每个用户的各个参数信息
    """
    variable = []

    for mFriend in friends[1:]:
        value = mFriend[var]
        variable.append(value)
    return variable


def get_all_profile(friends):
    """
    获取好友列表的 昵称、性别、省份、城市、签名
    其中所有好友昵称组合成一个list,所有好友的性别组合成一个list，所有好友的省份组合成一个list
    :param friends: 用户的好友列表
    :return: 返回一个DataFrame格式的数据集合
    """
    # 调用函数得到各变量，并把数据存到csv文件中，保存到桌面
    NickName = get_friend_value(friends, 'NickName')  # 用户昵称
    Sex = get_friend_value(friends, 'Sex')  # 性别信息
    Province = get_friend_value(friends, 'Province')  # 省份信息
    City = get_friend_value(friends, 'City')  # 城市信息
    Signature = get_friend_value(friends, 'Signature')  # 签名信息

    data = {'NickName': NickName, 'Sex': Sex, 'Province': Province, 'City': City, 'Signature': Signature}

    # 组合完成数据
    from pandas import DataFrame
    frame = DataFrame(data)
    frame.to_csv('data.csv', index=True)
    return frame


def get_all_signature(friends):
    """
    获取到所有的用户属性，组合成字符串，并生成词云
    strip():用于移除字符串头尾指定的字符,默认的是空格
    replace("span",""):用于去掉签名里面的span
    根据用户的签名，我们生成词云
    """
    import re
    siglist = []

    for mFriend in friends:
        signature = mFriend['Signature'].strip().replace("span","").replace("class","").replace("emoji","")
        rep = re.compile("1f\d+\w*|[<>/=]]")
        signature = rep.sub("", signature)
        siglist.append(signature)
    text = "".join(siglist)
    return text


def spilt_words_jieba(text):
    """
    使用jieb对词语进行分词
    :param text:
    :return:
    """

    import jieba
    word_list = jieba.cut(text, cut_all=True)
    word_space_split = " ".join(word_list)
    #print("这个值:"+ word_space_split)
    return word_space_split


def drar_word_cloud(word_space_split):
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud, ImageColorGenerator
    import numpy as np
    import PIL.Image as Image
    path = 'E:\website\PythonShizhanPractice\wordcloud_demo\msyh.ttf'
    # 读入背景图片
    abel_mask = np.array(Image.open("E:\website\PythonShizhanPractice\spide_wechatfriend_demo\wechat.jpg"))  # 生成

    print('+----------------加载图片成功！----------+')

    # my_wordcloud = WordCloud().generate(wl_space_split) 默认构造函数
    my_wordcloud = WordCloud(background_color='white',  # 设置背景颜色
                             max_words=200,     # 设置最大现实的字数
                             mask=abel_mask,  # 设置背景图片
                             max_font_size=60,   # 设置字体最大值
                             random_state=42,    # 设置有多少种随机生成状态，即有多少种配色方案
                             scale=2,
                             font_path=path).generate(word_space_split)  # 设置字体格式，如不设置显示不了中文

    # 根据图片生成词云颜色
    image_colors = ImageColorGenerator(abel_mask)

    plt.imshow(my_wordcloud.recolor(color_func=image_colors))

    plt.imshow(my_wordcloud)

    plt.axis("off")
    plt.show()
    my_wordcloud.to_file("E:\website\PythonShizhanPractice\spide_wechatfriend_demo\wechat_1.jpg")


def main():
    friends = fetch_friends_list()

    #count_friens_sex(friends)

    text = get_all_signature(friends)

    word_space_split = spilt_words_jieba(text)

    drar_word_cloud(word_space_split)

if __name__ == '__main__':
    main()
