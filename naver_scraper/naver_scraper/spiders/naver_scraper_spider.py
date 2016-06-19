import scrapy
from naver_scraper.items import NaverScraperItem

class NaverBlogSpider(scrapy.Spider):
    name = "naverblog"
    allowed_domains = ["naver.com"]
    start_urls = [
        "http://blog.naver.com/kdk926/PostList.nhn?from=postList&blogId=kdk926&currentPage=9999",
    ]

    def parse(self, response):
        # find form and fill in
        # call inner parse to parse real results.
        num = int(response.xpath("//table[@class='page-navigation']/tr/td[@class='cnt']/a/text()").extract()[-1])
        for idx in range(1, num):
            request = scrapy.FormRequest("http://blog.naver.com/kdk926/PostList.nhn?from=postList&blogId=kdk926&currentPage="+ str(idx),
                                         callback=self.parse_blog)
            yield request

    def parse_blog(self, response):
        for e in response.xpath("//*[@class='resultadosNumeroSuc']"):
                naverscraperItem = NaverScraperItem()
                naverscraperItem['title'] = e.xpath("../*[@class='resultadosTextWhite']/text()").extract()[0]
                naverscraperItem['detail'] = e.xpath("../*[@class='resultadosTextWhite']/text()").extract()[0]
                naverscraperItem['created_date'] = e.xpath("../*[@class='resultadosTextWhite']/text()").extract()[0]
                naverscraperItem['categorys.name'] = e.xpath("../*[@class='resultadosTextWhite']/text()").extract()[0]
        yield naverscraperItem