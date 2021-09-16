from urllib.parse import urlencode

import scrapy

queries = ['Vance+ME']


def get_url(url):
    payload = {'api_key': '3ce5047fa518a9aa8eb1a90891306b71', 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class GooglescholarSpider(scrapy.Spider):
    name = 'googlescholar'
    allowed_domains = ['scholar.google.com']
    start_urls = ['http://scholar.google.com/']

    def start_requests(self):
        for query in queries:
            url = 'https://scholar.google.com/scholar?' + urlencode({'hl': 'en', 'q': query})
            yield scrapy.Request(get_url(url), callback=self.parse, meta={'position': 0})

    def parse(self, response):
        position = response.meta['position']
        for res in response.xpath('//*[@data-rp]'):
            link = res.xpath('.//h3/a/@href').extract_first()
            temp = res.xpath('.//h3/a//text()').extract()
            if not temp:
                title = "[C] " + "".join(res.xpath('.//h3/span[@id]//text()').extract())
            else:
                title = "".join(temp)
            snippet = "".join(res.xpath('.//*[@class="gs_rs"]//text()').extract())
            published_data = "".join(res.xpath('.//div[@class="gs_a"]//text()').extract())
            position += 1
            item = {'title': title, 'publishedData': published_data, 'snippet': snippet}
            yield item
        next_page = response.xpath('//td[@align="left"]/a/@href').extract_first()
        if next_page:
            url = "https://scholar.google.com" + next_page
            yield scrapy.Request(get_url(url), callback=self.parse, meta={'position': position})

