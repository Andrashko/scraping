import scrapy
import logging

class StaffSpider(scrapy.Spider):
    name = "test"
    start_urls = ["https://www.uzhnu.edu.ua/uk/cat/faculty"]

    def __init__(self, name=None, **kwargs):
        self.p = kwargs.get("p")
        super().__init__(name, **kwargs)

    def parse(self, response):
        logging.warning(f"{'!'*50} {self.p}")