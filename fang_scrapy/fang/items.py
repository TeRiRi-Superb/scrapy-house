# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FangItem(scrapy.Item):
    json_name = scrapy.Field()
    # 省份
    sheng = scrapy.Field()
    # 城市名
    city_name = scrapy.Field()
    # 小区名
    fang_name = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 几居室
    rooms = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 联系电话
    phone = scrapy.Field()

