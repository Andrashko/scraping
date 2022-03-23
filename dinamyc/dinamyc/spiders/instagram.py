from wsgiref import headers
import scrapy
from dinamyc.SeleniumRequest import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 
from dinamyc.items import DinamycItem

from selenium.webdriver.support.ui import WebDriverWait

class InstagramSpider(scrapy.Spider):
    name = "instagram"
    start_urls = ["https://www.instagram.com/"]

    def start_requests(self):
                
        
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=1000,
                wait_until=expected_conditions.element_to_be_clickable(
                   ( By.CSS_SELECTOR,
                    "a li button")
                ),
                cookies={
                    "sessionid":"11817601325%3AEE7XKuDFYIzJvB%3A20"
                },
                # headers={
                #     "Access-Control-Allow-Origin":"*"
                # },
                execute=self.login
            )

    def login(self, driver):
        driver.refresh()
        WebDriverWait(
            driver=driver,
            timeout=10
        ).until(
            expected_conditions.element_to_be_clickable(
                   ( By.TAG_NAME,
                    "button")
            )
        )
        
        later_button = driver.find_element(By.XPATH, "//button[contains(text(),'Не зараз')]")
        if later_button:
            later_button.click()


       

    def parse(self, response, **kwargs):
        for img in response.css("li img"):
            yield DinamycItem(url=img.css('::attr(src)').get())
    