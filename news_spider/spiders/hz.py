from io import BytesIO

import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from news_spider.items import hzItem
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import time
import sava2Hbase
import base64

start = time.time()
global num
num=0

#记录层数
global level
level=1

#当前爬取层数
global now_level
now_level=1

#外链解析中的链接采用键值对存储，链接作为key，层数作为values，可以通过控制values的上限控制其爬取层数
global url_dic
url_dic={}

#存储图片url
global img_src_list
img_src_list=[]

#存储图片字节数组
global img_content_list
img_content_list=[]



#截图脚本
# script_png = """
#                 function main(splash, args)
#                 splash:go(splash.args.url)
#                 splash:set_viewport_size(1500, 10000)
#                 local scroll_to = splash:jsfunc("window.scrollTo")
#                 scroll_to(0, 2800)
#                 splash:wait(8)
#                 return {png=splash:png()}
#                 end
#                 """

class HzSpider(scrapy.Spider):
    name = 'hz'

    def start_requests(self):
        url = 'https://www.hangzhou.com.cn/'
        yield scrapy.Request(url, self.parse)
        #截图
        #yield SplashRequest(url, self.pic_save, endpoint='execute', args={'lua_source': script_png, 'images': 0})

    #保存截图
    # def pic_save(self, response):
    #     global num
    #     num=num+1
    #     #截图命名
    #     fname = 'hangzhouwang'+str(num) +'.png'
    #     with open(fname, 'wb') as f:
    #          f.write(base64.b64decode(response.data['png']))

    def links_return(self, response):
        link = LinkExtractor()
        links = link.extract_links(response)
        return links

    def link_add(self, links):
        global level
        global url_dic
        for link in links:
            key = link.url
            url_dic[key]= level
        level = level + 1
        return url_dic

    def pic_find(self, response):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        pic_list = soup.find_all('img')
        return pic_list

    def url_edit(self,pic):
        url = pic
        head = 'http'
        if head in url:
            pic = url
        else:
            pic = 'http:' + url

        return pic

    def parse(self, response):
        global level
        global now_level
        global url_dic
        global img_content_list
        global img_src_list

        pic_list = self.pic_find(response)

        item = hzItem()
        item['img_name'] = 'hz'
        item['img_url'] = response.url
        item['html'] = response

        for pic in pic_list:
            pic_src = pic['src']
            src = self.url_edit(pic_src)

            img_src_list.append(src)
            # 获取图片响应
            pic_res = requests.get(src)

            if pic_res.status_code == 200:
                pic_res.encoding = 'gbk'
            d = BytesIO(pic_res.content)
            data = []
            while True:
                t = d.read(1)
                if not t:
                    break
                data.append(t)
            data = sava2Hbase.jb2jb(data)
            img_content_list.append(data)

        # 图片字节数组列表
        item['img_content'] = img_content_list
        # 图片url列表
        item['img_src'] = img_src_list

        yield item

        links = self.links_return(response)
        url_dic = self.link_add(links)

        if (now_level > 0 and level < 4):
            for key, values in url_dic.items():
                url = key
                if (values == now_level):
                    yield scrapy.Request(url, callback=self.parse)
                    #保存截图
                    #yield SplashRequest(url, self.pic_save, endpoint='execute',args={'lua_source': script_png, 'images': 0})
            now_level = now_level + 1




