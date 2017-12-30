# -*- encoding:utf-8 -*-
"""
从花瓣网爬图片

"""
import requests
import os,time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
import lxml.html

'''
这个意思是模拟浏览的时候不加载图片和缓存，这样运行速度会加快一些
'''
# SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']  # 这
'''
下面是设置webdriver的种类，就是使用什么浏览器进行模拟，可以使用火狐来看它模拟的过程，也可以是无头浏览器PhantomJS来
快速获取资源
'''
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

browser = webdriver.Chrome()  # 使用什么浏览器进行模拟

wait = WebDriverWait(browser, 10)  # 最大等待浏览器加载为10秒，主要是为了等候AJAX

browser.set_window_size(1400,900)  # 设置一下模拟浏览网页的大小


def parser(url, param):
    """
    这个函数用来解析网页，后面有几次都用用到这些代码，所以直接写一个函数会让代码看起来更整洁有序。函数有两个参数：一个是网址，
    另一个是显性等待代表的部分，这个可以是网页中的某些板块，按钮，图片等等..
    :param url: 网址，要访问的网址
    :param param: 用在显性等待部分参数，比如是网页的版块、按钮、图片
    :return: 返回一个经过lxml解析后的doc字符串
    """
    browser.get(url)
    """
    这两个人条件验证元素是否出现，传入的参数都是元组类型的locator，如(By.ID, 'kw')
    顾名思义，一个只要一个符合条件的元素加载出来就通过；另一个必须所有符合条件的元素都加载出来才行
    presence_of_element_located
    presence_of_all_elements_located
    """
    element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, param)))

    html = browser.page_source  # 这里是加载出来当前的页面内容
    """
    解析 html 的话最好使lxml.html.fromstring(html),返回的是lxml.html.HtmlElement，
    >>> doc = html.fromstring('<div><p>lorem <span>poium</span></p></div>')
    >>> doc.text_content()
    'lorem poium'
    第一步先启动浏览器，输入地址，然后获取页面内容，然后加载成HtmlElement格式，然后打印
    """
    doc = lxml.html.fromstring(html)

    # print(doc.text_content())

    return doc


def get_main_url():
    print("-----正在打开主页搜寻链接中-----")
    try:
        doc = parser('http://huaban.com/boards/favorite/beauty/', '#waterfall')
        """
        //title[@lang]  选取所有拥有名为 lang 的属性的 title 元素。
        //* 选取所有的元素
        //title[@*]  选取所有带有属性的title
        //title[@lang=’eng’]  选取所有title元素，且这些元素拥有值为eng的lang属性
        /bookstore/book[1] 选取属于bookstore子元素的第一个book元素
        """
        # '//*[@id="waterfall"]/div/a[1]/@href' 栏目名称
        name = doc.xpath('//*[@id="waterfall"]/div/a[1]/div[2]/h3/text()')  # 抓取到栏目的名称

        print('-----这次爬到的美女栏目名字是:{}'.format(name))

        u = doc.xpath('//*[@id="waterfall"]/div/a[1]/@href')  # 这个是栏目的URL
        print("-----这次爬到的相对地址是:{}".format(u))
        """
        例如，有两个列表：
        a = [1,2,3]
        b = [4,5,6]
        使用zip()函数来可以把列表合并，并创建一个元组对的列表
        zip(a,b) =[(1, 4), (2, 5), (3, 6)]
        """
        for item, file_name in zip(u, name):

            main_url = 'http://huaban.com'+item
            print("-----主链接已找到:{}".format(main_url))

            if '*' in file_name:
                file_name = file_name.replace('*','')

            download(main_url, file_name)

            time.sleep(1)
    except Exception as e:
        print(e)


def download(main_url, file_name):

    print("----------准备下载中----------")

    try:
        doc = parser(main_url, '#waterfall')

        if not os.path.exists('image\\' + file_name):
            print("----------创建文件夹----------")
            os.makedirs('image\\' + file_name)

            link = doc.xpath ('//*[@id="waterfall"]/div/a/@href')
            # print(link)
            i = 0
            for item in link:
                i += 1
                # 拼接2级菜单，进入到具体的库中
                minor_url = 'http://huaban.com' + item
                doc = parser(minor_url, '#pin_view_page')

                image_url = doc.xpath('//*[@id="baidu_image_holder"]/a/img/@src')  # 这个是小图片
                # test_url = doc.xpath('// *[ @ id = "board_pins_waterfall"] / a/img/@src')
                image_url2 = doc.xpath('//*[@id="baidu_image_holder"]/img/@src')   # 这个是大图片
                image_url += image_url2   # 把所有图片地址汇总

                # image_url =image_url2
                try:
                    pic_url = 'http:' + str(image_url[0])
                    print('-----正在下载第{}张图片，地址是:{}'.format(str(i), pic_url))
                    r = requests.get(pic_url)

                    filename = 'image\\{}\\'.format(file_name) + str(i) + '.jpg'

                    with open(filename, 'wb') as fo:
                        fo.write(r.content)
                        fo.close()
                    print('-------------第{}张图片保存完毕----------'.format(str(i)))
                    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                except Exception:
                    print("----------下载第{}张照片时出错了----------".format(str(i)))
                    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    except Exception:
        print("------进行下载时出错了!----------")

if __name__ == '__main__':
    get_main_url()
