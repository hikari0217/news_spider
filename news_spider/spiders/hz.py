import scrapy
from scrapy.linkextractors import LinkExtractor
from news_spider.items import hzItem
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import time
import base64

start = time.time()
global num
num=0

#记录层数
global i
i=1

#当前爬取层数
global now
now=1

#外链解析中的链接采用键值对存储，链接作为key，层数作为values，可以通过控制values的上限控制其爬取层数
global url_dic
url_dic={}

# script = """
#                 function main(splash, args)
#                   splash:go(args.url)
#                   local scroll_to = splash:jsfunc("window.scrollTo")
#                   scroll_to(0, 2800)
#                   splash:set_viewport_full()
#                   splash:wait(8)
#                   return {html=splash:html()}
#                 end
#                 """

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

class HzSpider(scrapy.Spider):
    name = 'hz'

    def start_requests(self):
        url = 'https://www.hangzhou.com.cn/'
        yield scrapy.Request(url, self.parse)
        yield SplashRequest(url, self.pic_save, endpoint='execute', args={'lua_source': script_png, 'images': 0})

    def pic_save(self, response):
        global num
        num=num+1
        #截图命名
        fname = 'hangzhouwang'+str(num) +'.png'
        with open(fname, 'wb') as f:
             f.write(base64.b64decode(response.data['png']))

    def links_return(self, response):
        link = LinkExtractor()
        links = link.extract_links(response)
        return links

    def link_add(self, links):
        global i
        global url_dic
        for link in links:
            key = link.url
            url_dic[key]= i
        i = i + 1
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
        global i
        global now
        global url_dic

        pic_list = self.pic_find(response)
        for pic in pic_list:
            item = hzItem()
            item['img_name'] = 'hz'
            pic_src = pic['src']
            item['img_src']=self.url_edit(pic_src)

            yield item

        links = self.links_return(response)
        url_dic = self.link_add(links)

        if (now > 0 and i < 4):
            for key, values in url_dic.items():
                url = key
                if (values == now):
                    yield scrapy.Request(url, callback=self.parse)
                    yield SplashRequest(url, self.pic_save, endpoint='execute',args={'lua_source': script_png, 'images': 0})
            now = now + 1




