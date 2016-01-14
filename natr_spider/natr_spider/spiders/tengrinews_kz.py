import scrapy
from natr_spider.items import NewsArticleItem


class TengrinewsKzSpider(scrapy.Spider):
    name = "tengrinews.kz"
    allowed_domains = ["tengrinews.kz"]
    start_urls = [
        "http://tengrinews.kz/money/predsedatel-pravleniya-KASE-ushel-s-posta-287088/",
        "http://tengrinews.kz/article/292/",
        "http://tengrinews.kz/conference/121/",
        "http://tengrinews.kz/events/na-dakare-pogib-vtoroy-chelovek-za-tri-dnya-287174/"
    ]

    def parse(self, response):
        item = NewsArticleItem()
        item['source'] = 'TengriNews.kz'
        item['url'] = response.url
        item['title'] = response.selector.css('.data').xpath('h1/text()').extract_first()
        item['date'] = response.selector.css('.data').css('span.date::text').extract_first()
        item['paragraphs'] = response.selector.css('.text').xpath('p/text()').extract()
        return item


class NurKzSpider(scrapy.Spider):
    name = "nur.kz"
    allowed_domains = ["nur.kz"]
    start_urls = [
        "http://www.nur.kz/1011115-propavshaya-v-almatinskoy-oblasti-devu.html",
        "http://www.nur.kz/1011255-kazakhstan-obmenyaetsya-uchastkami-terr.html",
    ]

    def parse(self, response):
        item = NewsArticleItem()
        item['source'] = 'Nur.kz'
        item['url'] = response.url
        item['title'] = response.selector.css('div.c__article_text').xpath('h2/text()').extract_first()
        item['date'] = response.selector.css('div.c__article_data').xpath('span/text()').extract_first()
        item['paragraphs'] = response.selector.css('div.c__article_text').xpath('p/text()').extract()
        return item