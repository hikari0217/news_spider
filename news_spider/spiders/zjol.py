import scrapy
from scrapy.linkextractors import LinkExtractor
from news_spider.items import hzItem
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import time
import base64

#启动splash

# 截图序号
global num
num = 0

# 记录层数
global level
level = 1

# 当前爬取层数
global now_level
now_level = 1

#外链解析中的链接采用键值对存储，链接作为key，层数作为values，可以通过控制values的上限控制其爬取层数
global url_dic
url_dic={}


script = """
                function main(splash, args)
                splash:go(args.url)
                local scroll_to = splash:jsfunc("window.scrollTo")
                scroll_to(0, 2800)
                splash:set_viewport_full()
                splash:wait(8)
                return {html=splash:html()}
                end 
        """

script_png = """
                function main(splash, args)
                splash:go(splash.args.url)
                splash:set_viewport_size(1500, 10000)                
                local scroll_to = splash:jsfunc("window.scrollTo")
                scroll_to(0, 2800)
                splash:wait(8)
                return {png=splash:png()}
                end
                """

class ZjolSpider(scrapy.Spider):
    name = 'zjol'

    def start_requests(self):
        url = 'https://www.zjol.com.cn/'
        yield SplashRequest(url, self.parse,  endpoint='execute', args={'lua_source': script, 'url': url})
        yield SplashRequest(url, self.pic_save, endpoint='execute', args={'lua_source': script_png, 'images': 0})

    def pic_save(self, response):
        with open('浙江在线.png', 'wb') as f:
             f.write(base64.b64decode(response.data['png']))

    def links_return(self, response):
        link = LinkExtractor()
        links = link.extract_links(response)
        return links

        # 加到待爬取列表里
    def link_add(self, links):
        global level
        global url_dic
        for link in links:
            key = link.url
            url_dic[key] = level
        level = level + 1
        return url_dic


    def pic_find(self, response):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        pic_list = soup.find_all('img')
        return pic_list

    def url_edit(self,pic):
        url =pic
        head = 'http'
        tag_url = 'zjol.com.cn'
        tag1 = 'static'
        if tag_url in url:
            if head in url:
                pic_url =url
            else:
                pic_url = 'http:'+url
        elif head in url:
            pic_url = url
        else:
            if tag1 in url:
                pic_url = 'https://' + url
            else:
                pic_url = 'https://img.zjol.com.cn/mlf/dzw' + url
        return pic_url

    def parse(self, response):
        global level
        global now_level
        pic_list = self.pic_find(response)
        for pic in pic_list:
            item = hzItem()
            item['img_name'] = 'zjol'
            pic_src = pic['src']
            item['img_src'] = self.url_edit(pic_src)
            yield item

        links = self.links_return(response)
        url_dic = self.link_add(links)
        # 改变i的值来控制爬取层数
        if (now_level > 0 and level < 4):
            for key, values in url_dic.items():
                url = key
                if (values == now_level):
                    yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': script, 'url': url})
                    yield SplashRequest(url, self.pic_save, endpoint='execute',args={'lua_source': script_png, 'images': 0})
            now_level = now_level + 1
