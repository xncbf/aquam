from gc import get_objects

import scrapy
import urllib.request
import re

from PIL import Image
from naver_scraper.items import NaverScraperItem, ImageItem, CategorysItem
from django.conf import settings


class NaverBlogSpider(scrapy.Spider):
    name = "naverblog"
    allowed_domains = ["naver.com"]
    start_urls = [
        "http://blog.naver.com/kdk926/PostList.nhn?from=postList&blogId=kdk926&currentPage=9999",
    ]
    replace_image = re.compile('<img.*?>')
    remove_blank = re.compile('<img src="http://static.naver.net/blank.gif.*?>')
    cleanr = re.compile("<.*?>")


    def parse(self, response):
        # find form and fill in
        # call inner parse to parse real results.
        num = int(response.xpath("//table[@class='page-navigation']/tr/td[@class='cnt']/a/text()").extract()[-1])
        for idx in range(1, num+1):
            request = scrapy.FormRequest("http://blog.naver.com/kdk926/PostList.nhn?from=postList&blogId=kdk926&currentPage="+ str(idx), callback=self.parse_blog)
            yield request

    def parse_blog(self, response):
        galleryItem=[]

        # 스마트 에디터
        for e in response.xpath("//td[@class='bcc']"):
            try:
                galleryItem = NaverScraperItem()
                categorysItem = CategorysItem()
                imageItem = ImageItem()
                galleryItem['title'] = e.xpath("..//h3/text()[2]").extract()[0]

                #body 재가공
                smart_body = e.xpath("..//div[@class='se_component_wrap sect_dsc __se_component_area']").extract()[0].replace('<br>', '\s')
                smart_body_remove_blank = re.sub(self.remove_blank, '', smart_body)
                detail = self.parse_download_image(smart_body_remove_blank)
                detail_replace_image = re.sub(self.replace_image, '{}', detail)
                detail_cleanr_list = re.sub(self.cleanr, '', detail_replace_image).split('{}')
                detail_complite =''
                for idx, f in enumerate(detail_cleanr_list):
                    detail_complite += f + '{' + str(idx) + '}'
                detail_complite = detail_complite.rsplit('{', 1)[0].strip()
                detail_complite = re.sub(r'[\t\r\n ]+', r' ', detail_complite).replace('\s', '\n')

                galleryItem['detail'] = detail_complite
                galleryItem['created_date'] = e.xpath("..//span[@class='se_publishDate pcol2 fil5']/text()").extract()[0].split('\n')[0].replace('.', '-', 2).replace('.', '')
                # YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] 형식이어야 합니다
                categorysItem['name'] = e.xpath("..//a[@class='pcol2']/text()").extract()[0].replace(' ', '')
                galleryItem['categorys'] = categorysItem['name']
                yield categorysItem
                yield galleryItem
                imageItem['gallery'] = galleryItem['title']
                imageItem['file'] = self.parse_image_url(smart_body_remove_blank)
                yield imageItem
            except:
                continue

        # 일반 에디터
        for e in response.xpath("//td[@class='bcc']"):
            try:
                galleryItem = NaverScraperItem()
                categorysItem = CategorysItem()
                imageItem = ImageItem()
                galleryItem['title'] = e.xpath("..//span[@class='pcol1 itemSubjectBoldfont']/text()[1]").extract()[0]


                #body 재가공
                normal_body = e.xpath("..//div[@id='postViewArea']").extract()[0].replace('<br>', '\s')
                normal_body_remove_blank = re.sub(self.remove_blank, '', normal_body)
                detail = self.parse_download_image(normal_body_remove_blank)
                detail_replace_image = re.sub(self.replace_image, '{}', detail)
                detail_cleanr_list = re.sub(self.cleanr, '', detail_replace_image).split('{}')
                detail_complite =''
                for idx, f in enumerate(detail_cleanr_list):
                    detail_complite += f + '{' + str(idx) + '}'
                detail_complite = detail_complite.rsplit('{', 1)[0].strip()
                detail_complite = re.sub(r'[\t\r\n ]+', r' ', detail_complite).replace('\s', '\n')

                galleryItem['detail'] = detail_complite
                galleryItem['created_date'] = e.xpath("..//p[@class='date fil5 pcol2 _postAddDate']/text()").extract()[0].replace('.', '-', 2).replace('.', '')
                # YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] 형식이어야 합니다
                categorysItem['name'] = e.xpath("..//a[@class='pcol2']/text()").extract()[0].replace(' ', '')
                galleryItem['categorys'] = categorysItem['name']
                yield categorysItem
                yield galleryItem
                imageItem['gallery'] = galleryItem['title']
                imageItem['file'] = self.parse_image_url(normal_body_remove_blank)
                yield imageItem
            except:
                continue

        return galleryItem

    def parse_download_image(self, response):
        # url = "http://postfiles1.naver.net/20141204_160/kdk926_14176651128371lr8c_JPEG/20141203_110254.jpg?type=w2"
        # file_name = 'D:/workspace/DjangoProjects/BlogWorkspace/aquam/media/images/abcd.jpg'
        #download_local_url = 'D:/workspace/DjangoProjects/BlogWorkspace/aquam/media/images/'    #windows test
        download_local_url = '/Users/user/Desktop/PycharmProjects/aquam/aquam/media/images/'    #mac test
        # download_local_url = settings.MEDIA_ROOT + '/images/'  #ubuntu
        replace_item = response
        for i in range(0, response.count('src="')):
            temp = response.split('src="')[i+1]
            url = temp.split('"')[0]
            file_name = url.split('/')[-1].split('?')[0].replace('%', '')
            download_url = download_local_url + file_name
            media_url = settings.MEDIA_URL + 'images/' + file_name
            replace_item = str(replace_item).replace(url, media_url)
            if ImageItem.django_model.objects.filter(file='images/' + file_name).count() == 0:    #이미지 중복확인
                urllib.request.urlretrieve(url, download_url)      #이미지 다운로드
        return replace_item

    def parse_image_url(self, response):
        image_list = []
        for i in range(0, response.count('src="')):
            temp = response.split('src="')[i+1]
            url = temp.split('"')[0]
            image_list.append('images/' + url.split('/')[-1].split('?')[0].replace('%', ''))
        return image_list
