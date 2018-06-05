from pymongo import MongoClient


class Database:
    DATABASE = None
    URI = 'mongodb://127.0.0.1:27017'

    @staticmethod
    def initialize():
        client = MongoClient(Database.URI)
        Database.DATABASE = client['webapp']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
