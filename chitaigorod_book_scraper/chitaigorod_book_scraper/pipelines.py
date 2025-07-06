# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from itemadapter import ItemAdapter


class ChitaigorodBookScraperPipeline:
    def process_item(self, item, spider):
        return item


class MongoPipeline:
    collection_name = 'scraped_books'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        item_dict = adapter.asdict()
        
        if item_dict.get('isbn'):
            self.db[self.collection_name].update_one(
                {'isbn': item_dict['isbn']},
                {'$set': item_dict},
                upsert=True
            )
        
        return item
