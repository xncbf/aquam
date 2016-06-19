# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class NaverScraperPipeline(object):
    def __init__(self):
        self.ids_seen = set()
    #몰라 예제에있던거
    def process_item(self, item, spider):
        item['address'] = self.cleanup_address(item['address'])
        item.save()
        return item

    #중복제거래
    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item