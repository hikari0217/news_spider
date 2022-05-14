import scrapy


class SouhuItem(scrapy.Item):
    img_src =scrapy.Field()
    img_name =scrapy.Field()
    img_url = scrapy.Field()
    img_content = scrapy.Field()
    html=scrapy.Field()

class hzItem(scrapy.Item):
    img_src = scrapy.Field()
    img_name = scrapy.Field()
    img_url = scrapy.Field()
    html = scrapy.Field()
    img_content = scrapy.Field()

class qqItem(scrapy.Item):
    img_src = scrapy.Field()
    img_name = scrapy.Field()
    img_url = scrapy.Field()
    html = scrapy.Field()
    img_content = scrapy.Field()

class zjolItem(scrapy.Item):
    img_src = scrapy.Field()
    img_name = scrapy.Field()
    img_url = scrapy.Field()
    html = scrapy.Field()
    img_content = scrapy.Field()

