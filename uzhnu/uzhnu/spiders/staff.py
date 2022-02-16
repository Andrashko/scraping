from unicodedata import name
import scrapy
from uzhnu.items import FacultyItem, DepartmetnItem

class StaffSpider(scrapy.Spider):
    name = "staff"
    BASE_URL = "https://www.uzhnu.edu.ua"
    start_urls = ["https://www.uzhnu.edu.ua/uk/cat/faculty"]

    def parse(self, response):
        for a in response.css(".departments_unfolded li a"):
            url =f"{self.BASE_URL}{a.css('::attr(href)').get()}"
            res = FacultyItem(
                url=url,
                name=a.css("a::text").get()
            )
            yield res
            yield scrapy.Request(
                url=url,
                callback=self.parse_dep,
                meta={
                    "faculty": res["name"]
                }
            )

    def parse_dep(self, response):
        for a in response.css(".departments li a"):
            url =f"{self.BASE_URL}{a.css('::attr(href)').get()}"
            res = DepartmetnItem(
                url=url,
                name=a.css("a::text").get(),
                faculty=response.meta["faculty"]
            )
            yield res
