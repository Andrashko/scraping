# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from sqlite3 import connect
from laptops.items import LaptopItem


class LaptopsPipeline:
    def process_item(self, item, spider):
        return item


class FilterExpensivePipeline:
    def open_spider(self, spider):
        self.max_price = spider.max_price

    def process_item(self, item, spider):
        if item["price"] < self.max_price:
            return item
        else:
            raise DropItem(f"{item['model']} is too expensive")


class CalculateUSDPricePipeline:
    def process_item(self, item, spider):
        COURSE = 31.60
        item["priceUSD"] = item["price"] / COURSE
        return item


class CalcVendorsPipline:
    def process_item(self, item, spider):
        vendor = item["model"].split()[0]
        if self.vendors.get(vendor):
            self.vendors[vendor] += 1
        else:
            self.vendors[vendor] = 1
        return item

    def open_spider(self, spider):
        self.vendors = {}

    def close_spider(self, spider):
        spider.logger.info(f"{'='*100}\n{self.vendors}\n{'='*100}")


class FilterUniquePipline:
    def open_spider(self, spider):
        self.unique_items = set()

    def process_item(self, item, spider):
        if item["model"] in self.unique_items:
            raise DropItem(f"Not unique {item['model']}")
        else:
            self.unique_items.add(item["model"])
            return item


class SaveToDbPipline:
    def open_spider(self, spider):
        self.connection = connect("hotline.db")
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        if isinstance(item, LaptopItem):
            for laptop in self.cursor.execute(
                "SELECT id, model FROM laptops WHERE model=?",
                [item["model"]]
            ):
                spider.logger.info(f"{item['model']} is in db, updating price")
                self.cursor.execute(
                    "UPDATE laptops SET price=?, priceUSD=? WHERE id=?",
                    [item["price"], item["priceUSD"], laptop[0]]
                )
                self.connection.commit()
                return item
            self.cursor.execute(
                "INSERT INTO laptops (model, price,  priceUSD, img_url, images) VALUES (?,?,?,?,?)",
                [item["model"], item["price"], item["priceUSD"],
                    item["img_url"], item["images"][0]["path"]]
            )
            self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.close()
