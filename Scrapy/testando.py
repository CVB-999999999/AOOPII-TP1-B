import pymongo
from pymongo import MongoClient
cluster = MongoClient("mongodb://localhost:27017/")
db = cluster["teste-B"]
collection = db["teste-B"]

noticia = 'ola'
d1 = '342'

post = {"Title": noticia, "Date": d1}

collection.insert_one(post)