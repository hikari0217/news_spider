from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
from news_spider.settings import IMAGES_STORE as IMGS

global i
i=0

class ImgsPipeLine(ImagesPipeline):
    def get_media_requests(self, item, info):
        for i in range(len(item['img_src'])):
            yield scrapy.Request(url=item['img_src'], meta={'item': item})


    def file_path(self, request, response=None, info=None, *, item=None):
        global i
        item = request.meta['item']
        filePath = item['img_name']+str(i)+'.jpg'
        i=i+1
        return filePath

    def item_completed(self, results, item, info):
        return item
