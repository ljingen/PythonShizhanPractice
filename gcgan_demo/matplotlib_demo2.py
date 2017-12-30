# -*- encoding:utf-8 -*-
"""
这个例子，给我们讲解了如何使用柱状图或者饼状图的例子
一个用ax命名的对象。在Matplotlib中，画图时有两个常用概念，一个是平时画图蹦出的一个窗口，这叫一个figure。Figure相当于一个大的画
布，在每个figure中，又可以存在多个子图，这种子图叫做axes。顾名思义，有了横纵轴就是一幅简单的图表。在上面代码中，先把figure定义
成了一个一行两列的大画布，然后通过fig.add_subplot()加入两个新的子图。subplot的定义格式很有趣，数字的前两位分别定义行数和列数，
最后一位定义新加入子图的所处顺序，当然想写明确些也没问题，用逗号分开即可。。
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['axes.titlesize'] = 20
mpl.rc('xtick', labelsize=16)
mpl.rcParams['ytick.labelsize'] = 16
mpl.rcParams['axes.labelsize'] = 16

mpl.rcParams['xtick.major.size'] = 0
mpl.rcParams['ytick.major.size'] = 0


# 包含了狗、猫和猎豹的最高奔跑速度，还有对应的可视化颜色
speed_map = {
    'dog': (48, '#7199cf'),
    'cat': (45, '#4fc4aa'),
    'cheetah': (120, '#e1a7a2')
}

# 创建一个图的容器，并定义图容器的名字
fig = plt.figure('Bar chart & Pie chart')

# 在整张图上加入一个子图，121的意思是一个1行2列的子图的第一个
# 在matplotlib.pyplot里面 ，优先级分别为 figure、axure、plot、show
ax = fig.add_subplot(121)
ax.set_title('Running speed - bar chart')

# 生成x轴每个元素的位置

xticks = np.arange(3)

# 定义柱状图的每个柱的宽度
bar_width = 0.5

# 动物的名称
animals = speed_map.keys()

# 奔跑的速度
speeds = [x[0] for x in speed_map.values()]

# 对应的颜色
colors = [x[1] for x in speed_map.values()]

# 画柱状图，横轴是动物标签的位置，纵轴是速度，定义柱的宽度，同时设置柱的边缘为透明
bars = ax.bar(xticks, speeds, width=bar_width, edgecolor='none')

# 设置y轴的标题
ax.set_ylabel('Speed(km/h)')

# x轴每个标签的具体位置，设置为每个柱的中央
ax.set_xticks(xticks+bar_width/2)

# 设置每个标签的名字
ax.set_xticklabels(animals)

# 设置x轴的范围
ax.set_xlim([bar_width/2-0.5, 3-bar_width/2])

# 设置y轴的范围
ax.set_ylim([0, 125])

# 给每个bar分配指定的颜色
for bar, color in zip(bars, colors):
    bar.set_color(color)

# 在122位置加入新的图
ax = fig.add_subplot(122)
ax.set_title('Running speed - pie chart')

# 生成同时包含名称和速度的标签
labels = ['{}\n{} km/h'.format(animal, speed) for animal, speed in zip(animals, speeds)]

# 画饼状图，并指定标签和对应颜色
ax.pie(speeds, labels=labels, colors=colors)

plt.show()
