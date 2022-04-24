import scrapy


class SouhuItem(scrapy.Item):
    img_src =scrapy.Field()
    img_name =scrapy.Field()

class NeteaseItem(scrapy.Item):
    img_src = scrapy.Field()
    img_name = scrapy.Field()

class hzItem(scrapy.Item):
    img_src = scrapy.Field()
    img_name = scrapy.Field()

class qqItem(scrapy.Item):
    img_src = scrapy.Field()
    img_name = scrapy.Field()

class zjolItem(scrapy.Item):
    img_src = scrapy.Field()
    img_name = scrapy.Field()

