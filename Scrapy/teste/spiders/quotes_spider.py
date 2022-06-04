import datetime
from sqlite3 import Timestamp
import scrapy
from cassandra.cluster import Cluster

import sys     
if "twisted.internet.reactor" in sys.modules: del sys.modules["twisted.internet.reactor"]

# Coneção ao Cassandra
cluster = Cluster(['localhost'])
session = cluster.connect('aoop')

# Prepared Statments Cassandra
insertCassandra = session.prepare("INSERT INTO wikipedia(id, link, title, content, dateTime, hash, nPalavras, caracteres) VALUES (blobAsTimeuuid(now()), ?, ?, ?, totimestamp(now()), ?, ?, ?);")

import pymongo
from pymongo import MongoClient
# To Run: scrapy crawl quotes -o quotes.jl

cluster = MongoClient("mongodb://localhost:27017/")
db = cluster["TP1-B"]
collection = db["TP1-B"]
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

        # Buscar o resumo do acontecimentocl
        else:
            title = response.css('h1.firstHeading::text').get()

            for quote in response.css('div.mw-parser-output'):
                for div in quote.css('p')[1:]:
            
                    resumo = div.get()
                    
                    # Tirar o link da response
                    r = str(response).split(' ')
                    r = r[1].split('>')

                    hashA = str(hash(quote.get()))

                    palavras = len((quote.get()).split())

                    caracteres = len(quote.get())
                    
                    yield {
                        'link': r[0],
                        'titulo': title,
                        'resumo': resumo,
                        'hash': hashA,
                        'palavras': palavras,
                        'caracteres': caracteres,
                    }

                    session.execute(insertCassandra, [r[0], title, resumo, hashA, palavras, caracteres])

                    #print('sjkbdsakjdkbjsa' + resumo)
                    post = {  'link': r[0],
                        'titulo': title,
                        'resumo': resumo,
                        'tempo' : datetime.datetime.now(),
                        'hash': hashA,
                        'palavras': palavras,
                        'caracteres': caracteres}
                    collection.insert_one(post)
                    break

        for a in links:
            next_page = 'https://en.wikipedia.org' + a

            # print('-> ' + next_page)

            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
