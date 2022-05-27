import scrapy

# To Run: scrapy crawl quotes -o quotes.jl


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://en.wikipedia.org/wiki/Main_Page',
    ]

    def parse(self, response):
        for quote in response.css('td'):

            for li in quote.css('ul'):

                yield {
                    'text': li.css('li').getall(),
                }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
