from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import time

settings = get_project_settings()

start = time.time()
print("开始爬图片")

crawler = CrawlerProcess(settings)

crawler.crawl('souhu')
crawler.crawl('qq')
crawler.crawl('hz')
crawler.crawl('zjol')

crawler.start()

end = time.time()
