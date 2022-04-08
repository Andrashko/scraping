import scrapy
from dynamic.SeleniumRequest import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions 
from dynamic.items import DynamicItem

class InstagramSpider(scrapy.Spider):
    name = "instagram"
    start_urls = ["https://www.instagram.com/"]

    def start_requests(self):   
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
                wait_until=expected_conditions.element_to_be_clickable(
                   (By.CSS_SELECTOR,
                    "li button")
                ),
                execute=self.login
            )

    def login(self, driver, wait):
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//input[@name="username"]')))
        username_input = driver.find_element(By.XPATH, '//input[@name="username"]')
        username_input.send_keys("UzhnuTest")
        username_password = driver.find_element(By.XPATH, '//input[@name="password"]')
        username_password.send_keys("UzhnuTestPassword")   
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        login_button.click()
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Не зараз')]")))
        later_button = driver.find_element(By.XPATH, "//button[contains(text(),'Не зараз')]")
        later_button.click()

    def parse(self, response):
        for img in response.css("li img"):
            url = img.css('::attr(src)').get()
            yield DynamicItem(
                url=url,
                file_urls=[url],
                image_urls=[url],
            )
 