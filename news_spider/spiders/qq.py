import scrapy
from news_spider.items import qqItem
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import time
import base64

#截图序号
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
class QqSpider(scrapy.Spider):
    name = 'qq'
    #allowed_domains = ['news.qq.com']
    #start_urls = ['https://www.qq.com/']

    def start_requests(self):
        url = 'https://www.qq.com/'
        yield SplashRequest(url, self.parse,  endpoint='execute', args={'lua_source': script, 'url': url})
        yield SplashRequest(url, self.pic_save, endpoint='execute', args={'lua_source': script_png, 'images': 0})


    def pic_save(self, response):
        global num
        num = num + 1
        fname = 'qq' + str(num) + '.png'
        with open(fname, 'wb') as f:
             f.write(base64.b64decode(response.data['png']))

    def links_return(self, response):
        global level
        global url_dic
        link = LinkExtractor()
        links = link.extract_links(response)

        return links

    #找到所有img标签
    def pic_find(self,response):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        pic_list = soup.find_all('img')
        return pic_list

    #加到待爬取列表里
    def link_add(self, links):
        global level
        global url_dic
        for link in links:
            key = link.url
            url_dic[key]= level
        level = level + 1
        return url_dic

    def url_edit(self, pic_src):
        head = 'http'
        if head in pic_src:
            pic_url = pic_src
        else:
            pic_url = 'http:' + pic_src
        return pic_url

    def parse(self, response):
        global level
        global now_level
        global url_dic
        pic_list = self.pic_find(response)
        for pic in pic_list:
            item = qqItem()
            item['img_name'] = 'qq'
            pic_src = pic['src']
            item['img_src']=self.url_edit(pic_src)
            item['img_url'] = response.url
            item['html'] = response
            yield item

            # 改变i的值来控制爬取层数
            if (now_level > 0 and level < 4):
                for key, values in url_dic.items():
                    url = key
                    if (values == now_level):
                        yield SplashRequest(url, self.parse, endpoint='execute',
                                            args={'lua_source': script, 'url': url})
                        yield SplashRequest(url, self.pic_save, endpoint='execute',
                                            args={'lua_source': script_png, 'images': 0})
                now_level = now_level + 1
