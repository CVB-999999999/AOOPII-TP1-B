import scrapy

# To Run: scrapy crawl quotes -o quotes.jl


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://en.wikipedia.org/wiki/Main_Page',
    ]

    def parse(self, response):

        links = []


        # Buscar os dados da pagina inicial
        if str(response) == '<200 https://en.wikipedia.org/wiki/Main_Page>':

            for quote in response.css('td')[2:-2]:
                for li in quote.css('ul')[:3]:

                    yield {
                        'links': li.css('b').css('a::attr(href)').getall(),
                        'articles': li.css('li').getall(),
                    }
                
                    links = li.css('b').css('a::attr(href)').getall()
                    articles = li.css('li').getall()

                    break

        # Buscar o resumo do acontecimento
        else:
            for quote in response.css('div.mw-parser-output'):
                for div in quote.css('p')[1:]:

                    yield {
                        'resumo': div.get(),
                    }
                
                    resumo = div.get()

                    print('sjkbdsakjdkbjsa' + resumo)

                    break

        for a in links:
            next_page = 'https://en.wikipedia.org' + a

            print('-> ' + next_page)

            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
