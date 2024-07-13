import scrapy
from zhanzhangtupian.items import ZhanzhangtupianItem

class TuSpider(scrapy.Spider):
    name = "tu"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://sc.chinaz.com/tupian/"]
    def parse(self, response):
        node_list = response.xpath('//div[@class="tupian-list com-img-txt-list"]/div[@class="item"]')
        for node in node_list:
            item = ZhanzhangtupianItem()
            item['src'] = "https:" + node.xpath('./img/@data-original').get()
            yield item

        # 模拟翻页
        part_url = response.xpath('/html/body/div[3]/div[3]/a[last()]/@href').extract_first()
        # index_20.html表示页数
        if part_url != 'index_20.html':
            next_url = response.urljoin(part_url)
            yield scrapy.Request(url=next_url, callback=self.parse)

