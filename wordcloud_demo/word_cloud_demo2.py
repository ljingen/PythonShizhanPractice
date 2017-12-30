# -*- encoding:utf-8 -*-
from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import jieba
import PIL
from matplotlib import pyplot as plt
import numpy as np


def wordcloudplot(txt):
    path = 'E:\website\PythonShizhanPractice\wordcloud_demo\msyh.ttf'

    # path = path.encode('gb18030')

    # backgroud_Image = plt.imread('E:\website\PythonShizhanPractice\wordcloud_demo\p6.jpg')

    alice_mask = np.array(PIL.Image.open('E:\website\PythonShizhanPractice\wordcloud_demo\p7.jpg'))

    print('+----------------加载图片成功！----------+')
    '''设置词云样式'''
    wordcloud = WordCloud(
        font_path=path,     # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
        background_color="white",  # 设置背景颜色
        margin=5,
        width=1800,
        height=800,
        mask=alice_mask,    # 设置背景图片
        max_words=2000,     # 设置最大现实的字数
        max_font_size=60,   # 设置字体最大值
        random_state=42)    # 设置有多少种随机生成状态，即有多少种配色方案

    wordcloud = wordcloud.generate(txt)
    print('+----------------开始加载文本！----------+')
    # 改变字体颜色
    # img_colors = ImageColorGenerator(backgroud_Image)
    # 字体颜色为背景图片的颜色
    # wordcloud.recolor(color_func=img_colors)
    # 显示词云图
    plt.imshow(wordcloud)
    # 是否显示x轴、y轴下标
    plt.axis("off")
    plt.show()
    # 获得模块所在的路径的
    # d = path.dirname(__file__)
    wordcloud.to_file("E:\website\PythonShizhanPractice\wordcloud_demo\she3.jpg")
    # 保存词云到对应路径
    # wordcloud.to_file(path.join(d, "she3.jpg"))
    print('生成词云成功!已经保存到')


def main():
    arr = []
    fo = open(r'E:\website\PythonShizhanPractice\wordcloud_demo\yes-minister.txt', 'r', encoding='utf-8').read()

    words = list(jieba.cut(fo))

    for word in words:
        if len(word) > 1:
            arr.append(word)
    txt = r' '.join(arr)

    wordcloudplot(txt)


if __name__ == '__main__':
    main()