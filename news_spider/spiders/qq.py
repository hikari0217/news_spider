import scrapy
from news_spider.items import qqItem
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import time
import base64
import binary_upload

start=time.time()

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
        with open('qq.png', 'wb') as f:
             f.write(base64.b64decode(response.data['png']))

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)
        pic_list = soup.find_all('img')
        head = 'http'
        for pic in pic_list:
            item = qqItem()
            item['img_name'] = 'qq'
            pic_src = pic['src']
            if head in pic_src:
                item['img_src'] = pic_src
            else:
                item['img_src'] = 'http:' + pic_src

            yield item
