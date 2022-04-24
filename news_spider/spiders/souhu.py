import scrapy
from news_spider.items import SouhuItem
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import base64
import binary_upload

#启动splash

#截图序号
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

#网页渲染脚本
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

#截图脚本
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

class SouhuSpider(scrapy.Spider):
    name = 'souhu'
    #allowed_domains = ['news.souhu.com']
    #start_urls = ['https://news.sohu.com/']

    def start_requests(self):
        url = 'https://news.sohu.com/'
        yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': script, 'url': url})
        yield SplashRequest(url, self.pic_save, endpoint='execute', args={'lua_source': script_png, 'images': 0})

    #保存截图
    def pic_save(self, response):
        global num
        num=num+1
        #截图命名
        fname = 'souhu'+str(num) +'.png'
        with open(fname, 'wb') as f:
             f.write(base64.b64decode(response.data['png']))

    #返回页面中所有链接
    def links_return(self, response):
        global i
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
        global i
        global url_dic
        for link in links:
            key = link.url
            url_dic[key]= i
        i = i + 1
        return url_dic

    def url_edit(self, pic_src):
        head = 'http'
        if head in pic_src:
            pic_url = pic_src
        else:
            pic_url = 'http:' + pic_src
        return pic_url

    def parse(self, response):
        global i
        global now
        global url_dic
        pic_list = self.pic_find(response)
        for pic in pic_list:
            item = SouhuItem()
            item['img_name'] = 'souhu'
            pic_src = pic['src']
            item['img_src'] = self.url_edit(pic_src)
            yield item

        links = self.links_return(response)
        url_dic=self.link_add(links)
        #改变i的值来控制爬取层数
        if (now > 0 and i<4):
            for key, values in url_dic.items():
                url = key
                if (values==now):
                    yield SplashRequest(url, self.parse,  endpoint='execute', args={'lua_source': script, 'url': url})
                    yield SplashRequest(url, self.pic_save, endpoint='execute', args={'lua_source': script_png, 'images': 0})
            now=now+1