# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import pymongo

class TextPipeline(object):

    def process_item(self, item, spider):
        if item.get('listeners'):
            item["listeners"] = self.clean_listeners(item["listeners"])
            return item
        else:
            raise DropItem("Missing listeners in %s" % item)

    def clean_listeners(self, string_):
        if string_ is not None: 
            #return " ".join(string_.split())
            return int("".join(string_.split()).replace(',', '')) #nettoie les espaces superflus et convertit en entier
        

class MongoPipeline(object):

    collection_name = 'artists_collection'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb://mongo:27017")
        self.db = self.client["artists"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


