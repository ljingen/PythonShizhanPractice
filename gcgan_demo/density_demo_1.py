# -*- encoding:utf-8 -*-
"""
这个模块的主要功能是生成一个二维的图像，使用到了matplotlib.pyplot.subplots()
"""
from functools import partial
import numpy as np
from matplotlib import pyplot as plt

"""
Define a PDF 定义一个pdf

图中左边是一个自定义的概率密度函数，右边是相应的1w个样本的直方图，自定义分布和生成这些样本的代码如下
"""
# 生成一个从 -3 到3.01  步进是0.01的数组，(不包含3.01) 结果是 array([-3.00000000e+00,   -2.99000000e+00,])
x_samples = np.arange(-3, 3.01, 0.01)
'''
建立一个3×3的单位矩阵e, e.shape为（3，3），表示3行3列,第一维的长度为3，第二维的长度也为3
建立一个一维矩阵b,b =array([1,2,3,4])  b.shape=4 为矩阵的长度
numpy.empty(x,y)的作用是生成一个 x行y列的数组
'''
PDF = np.empty(x_samples.shape)  # 这生成一个 601个数据的一维数组
'''
布尔型索引:当前行中符合的一行给取出来，例如：
 >>>languages = np.array(['c','perl','python','c','python','perl','java'])
 >>>data = np.random.randn(7,5)
 >>>data[languages == 'python']
 array([[-0.69165371, -2.54222671, -3.21942188, -0.79798456, -0.27872961],
       [-0.75535754,  0.31312654,  0.8220388 ,  0.70390257,  1.01196357]])
从上面的交互信息看来，languages是一个7行1列的向量，而数据是一个7行5列的向量。布尔索引实现的是通过列向量中的每个元素的布尔量
数值对一个与列向量有着同样行数的矩阵进行符合匹配。而这样的作用，其实是把列向量中布尔量为True的相应行向量给抽取了出来。
'''
PDF[x_samples < 0] = np.round(x_samples[x_samples < 0]+3.5)/3  # x_samples <0的值取出来，赋值为新的值

PDF[x_samples >= 0] = 0.5 * np.cos(np.pi * x_samples[x_samples >= 0]) + 0.5

PDF /= np.sum(PDF)

# Calculate approximated CDF 计算接近的CDF值
CDF = np.empty(PDF.shape)

cumulated = 0

for i in range(CDF.shape[0]):
    cumulated += PDF[i]
    CDF[i] = cumulated

# Generate samples
generate = partial(np.interp, xp=CDF, fp=x_samples)

u_rv = np.random.random(10000)

x = generate(u_rv)

# Visualization 进行可视化操作
'''
subplots() Create a figure and a set of subplots
subplot是为了在一张图里放多个子图，与Matlab里的subplot类似。p1 = plt.subplot(211) 或者 p1 = plt.subplot(2,1,1)， 
表示创建一个2行，1列的图，p1为第一个子图
'''
fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(9, 4))  # plt.supplots()这个是

ax0.plot(x_samples, PDF)

ax0.axis([-3.5, 3.5, 0, np.max(PDF)*1.1])

ax1.hist(x, 100)

plt.show()
