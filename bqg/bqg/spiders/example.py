import scrapy
from scrapy import Request
from scrapy.cmdline import execute
from scrapy.http.response.text import TextResponse
from urllib.parse import urljoin
import re


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['www.xbiquge.so']
    start_urls = ['https://www.xbiquge.so/']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)
        # yield Request(url='https://www.xbiquge.so/book/4/', callback=self.parse_index, dont_filter=True)

    def parse_index(self, response: TextResponse):
        print(response)
        meta = {}
        for url in response.xpath('''//div[@id="list"]/dl/dd/a/@href''').extract():
            novel_url = urljoin(response.url, url)
            novel_name = response.xpath('''//title/text()''').get().split('最新章节_')[-1].replace('_笔趣阁', '').replace(
                '全文无弹窗阅读', '')
            meta['novel_url'] = novel_url
            meta['novel_name'] = novel_name
            yield Request(url=novel_url, callback=self.parse_text, dont_filter=True, meta=meta)

    def parse_text(self, response: TextResponse):
        print(response)
        meta = response.meta
        title = response.xpath('''//title/text()''').get().strip().strip('-笔趣阁')
        content = '\n'.join(response.xpath('''//div[@id="content"]//text()''').extract()[1:-1])
        content = content.replace('\xa0', ' ')
        yield {
            "novel_url": meta['novel_url'],
            "novel_name": meta['novel_name'],
            "novel_title": title,
            "novel_content": content
        }

    def parse(self, response: TextResponse):
        for url in response.xpath('''//div/div[@class="nav"]/ul/li/a/@href''').extract():
            if url == '/':
                continue
            url = urljoin(response.url, url)
            yield Request(url=url, callback=self.parse_1, dont_filter=True)

    def parse_1(self, response: TextResponse):
        for div in response.xpath('//div[@class="l"]/div[@class="item"]/dl/dt'):
            # novel_name = div.xpath('./span/text()').get().strip()
            novel_link = div.xpath('./a/@href').get().strip()
            yield Request(url=novel_link, callback=self.parse_index, dont_filter=True)


if __name__ == '__main__':
    execute('scrapy crawl example'.split())
