# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter


class FangPipeline:
    def __init__(self):
        self.f = open('newhouse.json', 'wb')
        self.e = open('esf.json', 'wb')
        self.newhouse = JsonLinesItemExporter(self.f, ensure_ascii=False, encoding='utf-8')
        self.esf = JsonLinesItemExporter(self.e, ensure_ascii=False, encoding='utf-8')

    def process_item(self, item, spider):
        if item['json_name'] == 'newhouse':
            self.newhouse.export_item(item)
        else:
            self.esf.export_item(item)
        return item

    def close_spider(self, spider):
        self.f.close()
