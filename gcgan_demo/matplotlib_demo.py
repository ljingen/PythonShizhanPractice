# -*- encoding:utf-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


# 通过rcParams设置全局横纵轴字体大小
mpl.rcParams['xtick.labelsize'] = 16  # 这个生成x轴的字体大小
mpl.rcParams['ytick.labelsize'] = 16  # 这个是生成y轴的字体大小

np.random.seed(42)  # 这个代表如果下一个也是这个seed生成的随机数会相同

# x轴的采样点，在指定的间隔内返回均匀数字，start:开始数字，stop：结束的  num:生成的样本数，默认是50
x = np.linspace(0, 15, 100)  # numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)

# 通过下面曲线加上噪声生成数据，所及拟合模型就用y了....
y = 2*np.sin(x)+0.3*x**2
y_data = y + np.random.normal(scale=0.3, size=100)

# figure()指定图表名称
"""
matplotlib.pyplot.figure(num=None, figsize=None, dpi=None, 
facecolor=None, edgecolor=None, frameon=True, FigureClass=<class 'matplotlib.figure.Figure'>, **kwargs)
plt.figure(figsize=(8,4))
"""
plt.figure('data-1', figsize=(8, 4))
plt.xlabel("year")
plt.ylabel("hourse")  #设置绘图对象的各个属性
plt.title("data-2")  # 设置这个图片的标题

# ‘.’标明画散点图,每个散点的形状是个圆,最简单的沿坐标轴划线函数
plt.plot(x, y_data, '.')  # matplotlib.pyplot.plot() 画一条点形线形 plot x and y using blue circle markers

# 画模型的图，Plot函数默认画连线图
plt.figure('model')
plt.plot(x, y)

# 两个图画一起
plt.figure('data & model')

# 通过'k'指定线的颜色，lw指定线的宽度
# 第三个参数除了颜色也可以指定线形，比如'r--'表示红色虚线
# 更多属性可以参考官网：http://matplotlib.org/api/pyplot_api.html
plt.plot(x, y, 'k', lw=3)

# scatter可以更容易生成散点图
plt.scatter(x, y_data)

# 将当前figure的图保存到文件 result.png
plt.savefig('result.png')

#一定要加上这句才能让画好的图显示在屏幕上
plt.show()

