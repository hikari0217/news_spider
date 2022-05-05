from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

def main():
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    didntWorkSpider = ['souhu', 'qq', 'zjol', 'hz']

    for spider_name in process.spider_loader.list():
        if spider_name in didntWorkSpider :
            continue
        print("Running spider %s" % (spider_name))
        process.crawl(spider_name)
    process.start()

main()



# crawler = CrawlerProcess(settings)
#
# crawler.crawl('souhu')
# crawler.crawl('qq')
# crawler.crawl('hz')
# crawler.crawl('zjol')
#
# crawler.start()

