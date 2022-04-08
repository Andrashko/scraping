from dataclasses import dataclass
import scrapy
from laptops.items import LaptopItem


class LaptopSpider(scrapy.Spider):
    name = 'laptop'
    start_urls = ['https://hotline.ua/computer/noutbuki-netbuki/']
    max_price = 30000

    def __init__(self, name=None, **kwargs):
        if kwargs.get("max_price"):
            self.max_price = float(kwargs.get("max_price")) 
        super().__init__(name)


    def parse(self, response):
        for product in response.css("li.product-item"):
            model = product.css("p.h4 a::text").extract_first()
            price = product.css("div.price-md span.value::text").extract_first()
            img = product.css("img.img-product::attr(src)").extract_first()
            if img != None:
                img_url = "https://hotline.ua/"+img 

            if model != None and price != None:
                laptop = LaptopItem(
                    model = model.strip(),
                    price = float(price.replace("\xa0","")),
                    img_url = img_url,
                    image_urls = [img_url]
                )
                yield laptop
           
        
        next = response.css("a.next::attr(href)").extract_first()
        if next != None:
            next_url = "https://hotline.ua/computer/noutbuki-netbuki/"+next
            return scrapy.Request(url=next_url, callback=self.parse)