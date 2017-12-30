# -*- encoding:utf-8 -*-
from wordcloud import WordCloud
from matplotlib import pyplot as plt

file_name = "E:\website\PythonShizhanPractice\wordcloud_demo\yes-minister.txt"

with open(file_name, 'r', encoding='utf-8') as fo:
    my_text = fo.read()

word_cloud = WordCloud().generate(my_text)

plt.imshow(word_cloud, interpolation="bilinear")

plt.axis("off")

plt.show()
