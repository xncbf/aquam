from gc import get_objects

import scrapy
import urllib.request
from naver_scraper.items import NaverScraperItem, ImageItem, CategorysItem
from django.conf import settings



class NaverBlogSpider(scrapy.Spider):
    name = "naverblog"
    allowed_domains = ["naver.com"]
    start_urls = [
        "http://blog.naver.com/kdk926/PostList.nhn?from=postList&blogId=kdk926&currentPage=9999",
    ]
    imageItem = ImageItem()

    def parse(self, response):
        # find form and fill in
        # call inner parse to parse real results.
        num = int(response.xpath("//table[@class='page-navigation']/tr/td[@class='cnt']/a/text()").extract()[-1])
        for idx in range(1, num+1):
            request = scrapy.FormRequest("http://blog.naver.com/kdk926/PostList.nhn?from=postList&blogId=kdk926&currentPage="+ str(idx),
                                         callback=self.parse_blog)
            yield request

    def parse_blog(self, response):
        galleryItem=[]

        # 스마트 에디터
        for e in response.xpath("//td[@class='bcc']"):
            try:
                galleryItem = NaverScraperItem()
                categorysItem = CategorysItem()
                self.imageItem = ImageItem()
                galleryItem['title'] = e.xpath("..//h3/text()[2]").extract()[0]
                smart_body = e.xpath("..//div[@class='se_component_wrap sect_dsc __se_component_area']").extract()[0]
                galleryItem['detail'] = self.parse_download_image(smart_body)
                galleryItem['created_date'] = e.xpath("..//span[@class='se_publishDate pcol2 fil5']/text()").split('\n')[0].extract()[0].replace('.', '-', 2).replace('.', '')
                categorysItem['name'] = e.xpath("..//a[@class='pcol2']/text()").extract()[0]
                galleryItem['categorys'] = categorysItem['name']
                self.imageItem.django_model.gallery_id = galleryItem['title']
                yield categorysItem
                yield galleryItem
                yield self.imageItem
            except:
                continue

        # 일반 에디터
        for e in response.xpath("//td[@class='bcc']"):
            try:
                galleryItem = NaverScraperItem()
                categorysItem = CategorysItem()
                self.imageItem = ImageItem()
                galleryItem['title'] = e.xpath("..//span[@class='pcol1 itemSubjectBoldfont']/text()[1]").extract()[0]
                normal_body = e.xpath("..//div[@id='postViewArea']").extract()[0]
                galleryItem['detail'] = self.parse_download_image(normal_body)
                galleryItem['created_date'] = e.xpath("..//p[@class='date fil5 pcol2 _postAddDate']/text()").extract()[0].replace('.', '-', 2).replace('.', '')
                # YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] 형식이어야 합니다
                categorysItem['name'] = e.xpath("..//a[@class='pcol2']/text()").extract()[0]
                galleryItem['categorys'] = categorysItem['name']
                self.imageItem.django_model.gallery_id = galleryItem['title']
                yield categorysItem
                yield galleryItem
                yield self.imageItem
            except:
                continue

        return galleryItem

    def parse_download_image(self, item):
        # url = "http://postfiles1.naver.net/20141204_160/kdk926_14176651128371lr8c_JPEG/20141203_110254.jpg?type=w2"
        # file_name = 'D:/workspace/DjangoProjects/BlogWorkspace/aquam/media/images/abcd.jpg'
        download_local_url = 'D:/workspace/DjangoProjects/BlogWorkspace/aquam/media/images/'    #windows test
        # download_local_url = settings.MEDIA_ROOT + '/images/'  #ubuntu
        replace_item = item
        self.imageItem['file'] = []
        for i in range(0, item.count('src="')):
            temp = item.split('src="')[i+1]
            url = temp.split('"')[0]
            file_name = download_local_url + url.split('/')[-1].split('?')[0]
            urllib.request.urlretrieve(url, file_name)      #이미지 다운로드
            media_url = settings.MEDIA_URL + 'images/' + url.split('/')[-1].split('?')[0]
            replace_item = str(replace_item).replace(url, media_url)
            self.imageItem['file'].append('images/' + url.split('/')[-1].split('?')[0])
        return replace_item
