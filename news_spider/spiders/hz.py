import scrapy
from scrapy.linkextractors import LinkExtractor
from news_spider.items import hzItem
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import time
import base64
import binary_upload

start = time.time()
global num
num=0

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

    def pic_find(self, response):
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        pic_list = soup.find_all('img')
        return pic_list

    def parse(self, response):
        global i
        pic_list = self.pic_find(response)
        head = 'http'
        for pic in pic_list:
            item = hzItem()
            item['img_name'] = 'hz'
            pic_src = pic['src']
            if head in pic_src:
                item['img_src'] = pic_src
            else:
                item['img_src'] = 'http:' + pic_src

            yield item

        # links = self.links_return(response)
        # for link in links:
        #     yield scrapy.Request(link.url, callback=self.parse)

