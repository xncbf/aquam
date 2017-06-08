from django.core.management import call_command
from django.utils import timezone
from aquam.celery import app
from ..naver_scraper.naver_scraper.spiders.naver_scraper_spider import NaverBlogSpider
from scrapy.crawler import CrawlerProcess


@app.task
def get_ses_statistics():
    call_command('get_ses_statistics')


@app.task
def crawl_naver_blog():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(NaverBlogSpider)
    process.start()
