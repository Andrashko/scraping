import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scopus.items import ScopusItem
from json import load
from time import sleep


class PublicationsSpider(scrapy.Spider):
    name = 'publications'
    start_urls = []
    default_headers = {
        # "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "accept-language":"uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6",
    }

    def start_requests(self):
        f = open("list.json", encoding='utf-8')
        sci = load(f)
        f.close()
        for s in sci:
            if s.get("profiles").get("scopus"):
                sleep(5)
                yield SeleniumRequest(
                    url=s.get("profiles").get("scopus"),
                    callback=self.parse,
                    wait_time=15,
                    wait_until=EC.element_to_be_clickable(
                        (By.XPATH, '//li[@data-component="results-list-item"]')),
                    headers=self.default_headers,
                    meta={"name": s.get("name")}
                )

    def parse(self, response):
        try:
            sci = ScopusItem()
            sci["name"] = response.meta["name"]
            sci["keywords"] = []
            sci["publications"] = []
            # with open("index.html", "w", encoding="utf-8") as file:
            #     file.write(str(response.xpath('//li[@data-component="results-list-item"]').getall()))
            dig = response.xpath(
                './/div[@class="col-lg-6 col-24"]//h3/text()').getall()
            sci["documents"] = int(dig[0]),
            sci["citations"] = int(dig[1][0]),
            sci["h"] = int(dig[2][0]),
            for row in response.xpath('//li[@data-component="results-list-item"]'):
                pub = {
                    "title": " ".join(row.xpath(".//h5//text()").getall()),
                    "journal": row.xpath('.//span[@data-component="document-source-title"]/text()').get(),
                    "meta": row.xpath('.//span[@class="text-meta"]/text()').get(),
                    "citations": int(row.xpath('.//span[@class="info-field__value sc-els-info-field"]//text()').get()),
                    "coauthors": []
                }
                for a in row.xpath('.//*[@data-component="document-authors"]//a'):
                    author = {
                        "name": a.xpath('.//text()').get(),
                        "url": a.xpath('./@href').get()
                    }
                    pub["coauthors"].append(author)
                sci["publications"].append(pub)

                # with open("temp.txt", "a", encoding="utf-8") as file:
                #     file.write(f"{title}\n")
                #     item = ScopusItem()
                #     item["title"] = title
                #     yield item

            for top in response.xpath('//button[@name="topicName"]'):
                for w in top.xpath('.//span/text()').get().split(";"):
                    sci["keywords"].append(w)

            yield sci
        except:
            yield {}
