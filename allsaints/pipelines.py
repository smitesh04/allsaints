# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from allsaints.items import storeLocatorItem, dataItem
from allsaints.db_config import DbConfig
obj = DbConfig()

class AllsaintsPipeline:
    def process_item(self, item, spider):
        if isinstance(item, storeLocatorItem):
            obj.insert_store_table(item)
        if isinstance(item, dataItem):
            id = item['id']
            del item['id']
            obj.insert_data_table(item)
            obj.update_store_status(id)
        return item


