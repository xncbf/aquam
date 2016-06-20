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
        naverscraperItem=[]

        # 스마트 에디터
        for e in response.xpath("//td[@class='bcc']"):
            try:
                naverscraperItem = NaverScraperItem()
                naverscraperItem['title'] = e.xpath("..//h3/text()[2]").extract()[0]
                naverscraperItem['detail'] = e.xpath("..//div[@class='se_component_wrap sect_dsc __se_component_area']").extract()[0]
                naverscraperItem['created_date'] = e.xpath("..//span[@class='se_publishDate pcol2 fil5']/text()").extract()[0]
                # naverscraperItem['categorys.name'] = e.xpath("..//div[@class='se_series']/*/text()").extract()[0]
                # naverscraperItem['categorys_id'] = '1'
                yield naverscraperItem
            except:
                continue

        # 일반 에디터
        for e in response.xpath("//td[@class='bcc']"):
            try:
                naverscraperItem = NaverScraperItem()
                naverscraperItem['title'] = e.xpath("..//span[@class='pcol1 itemSubjectBoldfont']/text()[1]").extract()[0]
                naverscraperItem['detail'] = e.xpath("..//div[@id='postViewArea']").extract()[0]
                naverscraperItem['created_date'] = e.xpath("..//p[@class='date fil5 pcol2 _postAddDate']/text()").extract()[0]
                # naverscraperItem['categorys.name'] = e.xpath("..//div[@class='se_series']/*/text()").extract()[0]
                # naverscraperItem['categorys_id'] = '1'
                yield naverscraperItem
            except:
                continue

        return naverscraperItem