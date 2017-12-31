# -*- encoding:utf-8 -*-
import requests, re
from lxml import etree


home_url = 'https://www.xinyongheimingdan.cc/'  # 设置要爬取信息的主站地址(中国信用黑名单)
cookies = {'PHPSESSID': '0bemughtu9sjmdc0c2p0nnq2s0',
           '__cfduid': 'd50e82d6acfe179c913b97e305ee44b2c1514699020',
           '__tins__15183126':'%7B%22sid%22%3A%201514699019967%2C%20%22vd%22%3A%2012%2C%20%22expires%22%3A%201514702368853%7D',
           '_ga': 'GA1.2.1922643652.1514699020',
           '_gat': '1',
           '_gid': 'GA1.2.773777402.1514699020'}  # 访问信用黑名单网站的登录cookies

home_response = requests.get(home_url, cookies=cookies)

home_html = home_response.text  # 把读取的网页内容取出来 localHref('pMmaPiRtD9')

# localHref('eNsrJvBcZ7')

href_geren = r"localHref\(\'(.*?)\'\)"

r_totle_page = r'共 [0-9]+'  # 正则表达式,获取一共有多少页

r_curent_page = r' \d+\/\d+ 页'  # 正则表达式,获取当前正好在哪个页面

h_re = re.compile(href_geren)  # 生成正则表达式

href_geren_all = h_re.findall(home_html)  # 选出所有符合的链接特征

totle_page_num = int(re.search(r_curent_page, home_html).group().split('/')[1].split(' ')[0])  # 取出一共有多少页
curent_page_num = int(re.search(r_curent_page, home_html).group().split('/')[0])  # 取出当前所在页数


for i in href_geren_all:  # 生成个人的属性页面
    profile_url = 'https://www.xinyongheimingdan.cc/blacklist-'+i+'.html' # 便利出来组合成个人页面的 url

    # get_url = requests.get(profile_url, headers={'cookies':cookies})

    profile_response = requests.get(profile_url, cookies=cookies)

    profile_HTML = profile_response.text.encode("utf-8")

    htmlOBJ = etree.HTML(profile_HTML)

    nameOBJ = htmlOBJ.xpath('//*[@id="body"]/div/div/div[2]/span[1]/text()')  # 名字

    sfzOBJ = htmlOBJ.xpath('//h3[@class="margin_top_15"]/span[@class="inline"]/i[1]/text()')  # 身份证

    phoneOBJ = htmlOBJ.xpath('//*[@id="body"]/div/div/h3[1]/span[2]/i/text()')  # 手机号
    wechatOBJ = htmlOBJ.xpath('//*[@id="body"]/div/div/div[3]/span[1]/text()')  # 微信
    alipayOBJ = htmlOBJ.xpath('//*[@id="body"]/div/div/div[3]/span[2]/text()')  # 支付宝
    all_info = nameOBJ, sfzOBJ, phoneOBJ, wechatOBJ, alipayOBJ

    print(all_info)