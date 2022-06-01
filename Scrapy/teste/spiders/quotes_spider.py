import scrapy
from cassandra.cluster import Cluster

import sys     
if "twisted.internet.reactor" in sys.modules: del sys.modules["twisted.internet.reactor"]

# Coneção ao Cassandra
cluster = Cluster(['localhost'])
session = cluster.connect('aoop')

# Prepared Statments Cassandra
insertCassandra = session.prepare("INSERT INTO wikipedia(id, link, title, content, dateTime) VALUES (blobAsTimeuuid(now()), ?, ?, ?, totimestamp(now()));")

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

                    # yield {
                    #     'links': li.css('b').css('a::attr(href)').getall(),
                    #     'articles': li.css('li').getall(),
                    # }
                
                    links = li.css('b').css('a::attr(href)').getall()
                    # articles = li.css('li').getall()

                    break

        # Buscar o resumo do acontecimento
        else:
            title = response.css('h1.firstHeading::text').get()

            for quote in response.css('div.mw-parser-output'):
                for div in quote.css('p')[1:]:
            
                    resumo = div.get()
                    
                    # Tirar o link da response
                    r = str(response).split(' ')
                    r = r[1].split('>')
                    
                    yield {
                        'link': r[0],
                        'titulo': title,
                        'resumo': resumo,
                    }

                    session.execute(insertCassandra, [r[0], title, resumo])

                    break

        for a in links:
            next_page = 'https://en.wikipedia.org' + a

            # print('-> ' + next_page)

            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
