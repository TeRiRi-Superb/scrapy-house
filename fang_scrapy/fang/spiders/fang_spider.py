import scrapy
import re
from fang.items import FangItem


class FangSpiderSpider(scrapy.Spider):
    name = 'fang_spider'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath('//div[@class="outCont"]//tr[position()<last()]')
        sheng = None
        for tr in trs:
            tds = tr.xpath('./td[not(@class)]')
            shengfen = tds[0]
            shengfen_text = shengfen.xpath('.//text()').get()
            shengfen_text = re.sub(r'\s', '', shengfen_text)
            if shengfen_text:
                sheng = shengfen_text
            citys = tds[1]
            citys_a = citys.xpath('./a')
            for city in citys_a:
                city_link = city.xpath('./@href').get()
                city_name = city.xpath('./text()').get()
                url_model = city_link.split('.')
                scheme = url_model[0]
                domain = url_model[1]
                com = url_model[2]
                newhouse_url = scheme + '.newhouse.' + domain + '.' + com + 'house/s/'
                esf_url = scheme + '.esf.' + domain + '.' + com
                yield scrapy.Request(url=newhouse_url, callback=self.parse_newhouse, meta={'info':(sheng, city_name)})
                yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={'info':(sheng, city_name)})


    def parse_newhouse(self, response):
        json_name = 'newhouse'
        sheng, city_name = response.meta.get('info')
        lis = response.xpath('//div[@class="nl_con clearfix"]/ul/li[@id or @onclick]')
        for li in lis:
            fang_name = li.xpath('.//a/img/@alt').get()
            address = li.xpath('.//div[@class="address"]/a/@title').get()
            area = li.xpath('.//div[@class="house_type clearfix"]/text()[last()]').get()
            area = re.sub(r'\s|－', '', area)
            rooms = li.xpath('.//div[@class="house_type clearfix"]/a/text()').getall()
            rooms = '/'.join(rooms)
            price = li.xpath('.//div[@class="nhouse_price"]//text()').getall()
            price = ''.join(price)
            price = re.sub(r'\s', '', price)
            phone = li.xpath('.//div[@class="tel"]/p//text()').getall()
            phone = ''.join(phone)
            item = FangItem(
                json_name=json_name,
                sheng=sheng,
                city_name=city_name,
                fang_name=fang_name,
                address=address,
                area=area,
                rooms=rooms,
                price=price,
                phone=phone,
            )
            yield item
        next_url = response.xpath('//li[@class="fr"]/a[@class="next" and position()>2]/@href').get()
        # active_num = response.xpath('//li[@class="fr"]/a[@class="active"]/text()').get()
        # active_url = response.xpath('//li[@class="fr"]/a[last()]/@href').get()
        # last_num = response.xpath('//li[@class="fr"]/a[last()]/text()').get()
        # print(next_url)
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_newhouse, meta={'info':(sheng, city_name)})

    def parse_esf(self, response):
        json_name = 'esf'
        sheng, city_name = response.meta.get('info')
        dls = response.xpath('//div[@class="shop_list shop_list_4"]/dl[not(@dataflag="bgcomare")]')
        for dl in dls:
            fang_name = dl.xpath('.//h4/a/span/text()').get().strip()
            address = dl.xpath('.//p[@class="add_shop"]/span/text()').get()
            area = dl.xpath('.//p[@class="tel_shop"]//text()').getall()
            area = ''.join(area)
            area = ''.join(re.findall(r'\d+㎡', area))
            rooms = dl.xpath('.//p[@class="tel_shop"]/text()').get().strip()
            price = dl.xpath('./dd[@class="price_right"]//text()').getall()
            price = list(map(lambda p:p.strip(), price))
            price = ''.join(price)
            phone = dl.xpath('.//span[@class="people_name"]/a/text()').get()
            item = FangItem(
                json_name=json_name,
                sheng=sheng,
                city_name=city_name,
                fang_name=fang_name,
                address=address,
                area=area,
                rooms=rooms,
                price=price,
                phone=phone,
            )
            yield item
        all_page_count = response.xpath('//div[@class="page_al"]/span[last()]/text()').get()
        all_page_count = str(re.findall(r'\d+', all_page_count))
        active_count = response.xpath('//div[@class="page_al"]/span[@class="on"]/text()').get()
        next_url = response.xpath('//div[@class="page_al"]/p[last()-1]/a/@href').get()
        if not active_count == all_page_count:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_esf, meta={'info': (sheng, city_name)})

