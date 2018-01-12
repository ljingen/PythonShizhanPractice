# -*- encoding:utf-8 -*-
"""
七牛云的人脸识别功能的python实现方式,需要先去注册自己的 secret 和 access key用于上传文件到七牛云的
空间进行处理,人像识别是七牛云的一项收费服务，项目价格为 1.5元/千次 ，测试前先存2元避免意外
"""
from functools import partial
import numpy
from skimage import transform

EPS = 1e-66  # 是的.10的-6次方.简单的说,就是1.0的小数点,向左边移动六次 是0.000001的意思

RESOLUTION = 0.001
num_grids = int(1/RESOLUTION + 0.5) #num_grids = 1000

ve = numpy.array([5,5,5,5])
def generate_lut(img):
    """
    谓偏函数即是规定了固定参数的函数,在函数式编程中我们经常可以用到 partial()
    linear approximation of CDF & margina
    :param img:density_img,即使用density_img = skimage.io.imread('inputs/batman.jpg',True)读取的图片
    :return:lut_y , lut_x
    """
    # skimage.transform.resize(image,output_shapre)， resize是改变图片的尺寸，其中image是需要改变尺寸的图片，output_shape
    # 新的图片尺寸，
    density_img = transform.resize(img, (num_grids, num_grids))  # 将img这个图片,按照新的num_grids,num_grids尺寸进行缩放
    """
      numpy.sum([[0,1,2,3],[2,1,3,2],[2,2,2,2]], axis=0)  >>>array([4, 4, 7, 7])
      numpy.sum([[0,1,2,3],[2,1,3,2],[2,2,2,2]], axis=1) >>>array([6, 8, 8])
      numpy.sum([[0,1,2,3],[2,1,3,2],[2,2,2,2]]) >>>22
    """
    x_accumlation = numpy.sum(density_img, axis=1)  # axis =1表示把行的都相加,然后做成一维数组
    print("合并后，新的一维数组的长度为 %d" % len(x_accumlation))
    sum_xy = numpy.sum(x_accumlation)  # 这个地方是把所有的x_accumlation都相加

    y_cdf_of_accumlation_x = [[0., 0.]]

    accumulated = 0
    """
    enumerate :还可以接收第二个参数，用于指定索引起始值
    list1 = ["这", "是", "一个", "测试"]
    for index, item in enumerate(list1, 1):
    print index, item
    >>>
    1 这
    2 是
    3 一个
    4 测试
    range(1,5,2) #代表从1到5，间隔2(不包含5)
    [1, 3]

    """
    for ir, i in enumerate(range(num_grids-1, -1, -1)):  # 这个代表从 num_grids-1 到-1,间隔是-1，(不包含-1)
        accumulated += x_accumlation[i]
        if accumulated == 0:
            print("第%d次循环,当前i是:%d--- accumulated==0时候我会被运行，现在accumulated是:%.2f" % (ir, i, accumulated))
            y_cdf_of_accumlation_x[0][0] = float(ir+1)/float(num_grids)
        elif EPS < accumulated < sum_xy-EPS:
            print("第%d次循环,当前i是:%d--- accumulated!=0时候我会被运行，现在accumulated是:%.2f" % (ir, i, accumulated))
            y_cdf_of_accumlation_x.append([float(ir+1)/float(num_grids), accumulated/sum_xy])
        else:
            print("第%d次循环,当前i是:%d--- accumulated>sum_xy时候我会被运行，现在accumulated是:%.2f" % (ir, i, accumulated))
            break

    y_cdf_of_accumlation_x.append([float(ir+1)/float(num_grids), 1.])

    #print("y轴是{}".format(y_cdf_of_accumlation_x))

    y_cdf_of_accumlation_x = numpy.array(y_cdf_of_accumlation_x)

    x_cdfs = []

    for j in range(num_grids):
        x_fred = density_img[num_grids-j-1]
        sum_x = numpy.sum(x_fred)
        x_cdfs = [[0., 0.]]
        accumulated = 0
        for i in range(num_grids):
            accumulated += x_fred[i]
            if accumulated == 0:
                x_cdfs[0][0] = float(i+1)/float(num_grids)
            elif EPS < accumulated < sum_xy-EPS:
                x_cdfs.append([float(i+1)/float(num_grids), accumulated/sum_x])
            else:
                break

        x_cdfs.append([float(i+1)/float(num_grids), 1.])

        if accumulated > EPS:
            x_cdf = numpy.array(x_cdfs)
            x_cdfs.append(x_cdf)
        else:
            x_cdfs.append(None)
    """
    numpy.interp()
    """
    y_lut = partial(numpy.interp, xp=y_cdf_of_accumlation_x[:, 1], fp=y_cdf_of_accumlation_x[:, 0])
    #print("我是y_lut:{}".format(y_lut))
    """
    x_luts = []
    for i in range(num_grids):
        if x_cdfs[i] is not None:
            x_lut= partial(numpy.interp, xp=x_cdfs[i][:, 1], fp=x_cdfs[i][:, 0])
            x_luts.append(x_lut)
        else:
            None
    """
    # 下面的语句使用的是列表推导式，类似于[x*x if x%3==0 else x*3 for x in range(10)]
    x_luts = [partial(numpy.interp, xp=x_cdfs[i][:, 1], fp=x_cdfs[i][:, 0]) if x_cdfs[i] is not None else None for i in range(num_grids)]

    return y_lut, x_luts


def sample_2d(lut, N):
    y_lut, x_luts = lut
    u_rv = numpy.random.random((N, 2))
    samples = numpy.zeros(u_rv.shape)
    for i, (x,y) in enumerate(u_rv):
        ys = y_lut(y)
        x_bin = int(ys/RESOLUTION)
        xs = x_luts[x_bin](x)
        samples[i][0] = xs
        samples[i][1] = ys
    return samples

if __name__ == '__main__':
    from skimage import io, data
    """
    读取单张彩色rgb图片，使用skimage.io.imread（fname）函数,带一个参数，表示需要读取的文件路径。
    显示图片使用skimage.io.imshow（arr）函数，带一个参数，表示需要显示的arr数组（读取的图片以numpy数组形式计算）
    """
    density_img = io.imread('inputs/random.jpg', True)  # 从文件中读取单个rgb文件

    lut_2d = generate_lut(density_img)

    print("这个是Lut_2d:{}".format(lut_2d))

    samples = sample_2d(lut_2d, 10000)

    from matplotlib import pyplot
    fig, (ax0, ax1) = pyplot.subplot(ncols=2, figsize=(9, 4))
    fig.cavas.set_window_title("Test 2D Sampling")
    ax0.imshow(density_img, cmap="gray")
    ax0.xaxis.set_major_locator(pyplot.NullLocator)
    ax0.yaxis.set_major_locator(pyplot.NullLocator)

    ax1.axis("equal")
    ax1.axis([0, 1, 0, 1])
    ax1.plot(samples[:, 0], samples[:, 1], "k,")
    pyplot.show()

