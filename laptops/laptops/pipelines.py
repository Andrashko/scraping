# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class LaptopsPipeline:
    def process_item(self, item, spider):
        return item

class FilterPipeline:
    def process_item(self, item, spider):
        if item["price"]<25000:
            return item
        else:
            raise DropItem(f"{item['model']} is too expancive")

class CalculateUSDPricePipeline:
    course = 31.60
    def process_item(self, item, spider):
        item["priceUSD"] = item["price"] / self.course
        return item

class CalcVendorsPipline:
    def process_item(self, item, spider):
        vendor = item["model"].split()[0]
        if self.vendors[vendor]:
            self.vendors[vendor] += 1
        else:
            self.vendors[vendor] = 1
        return item

    def open_spider(self, spider):
        self.vendors = {}
        
    def close_spider(self, spider):
        print("="*200)
        print (self.vendors)
        print("="*200)



class FilterUniquePipline:
    def open_spider(self, spider):
        self.unique_items = set()
    
    def process_item(self,item,spider):
        if item["model"] in self.unique_items:
            raise DropItem("Not unique")
        else:
            self.unique_items.add(item["model"])
            return item
