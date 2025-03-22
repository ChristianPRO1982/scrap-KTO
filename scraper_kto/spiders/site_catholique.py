import scrapy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from scrapy.http import HtmlResponse
import html

class SiteCatholiqueSpider(scrapy.Spider):
    name = "site_catholique"
    allowed_domains = ["site-catholique.fr"]
    start_urls = [
        "https://site-catholique.fr/?Prieres",
        "https://site-catholique.fr/?Chapelets",
        "https://site-catholique.fr/?Chemins-de-Croix",
        "https://site-catholique.fr/?Sacrements",
        "https://site-catholique.fr/?Humour",
        ]

    def start_requests(self):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)

        for url in self.start_urls:
            driver.get(url)
            
            # Scroll
            for _ in range(50):  
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                time.sleep(3)

            # Récupérer tout le HTML et le nettoyer
            page_source = html.unescape(driver.page_source)
            driver.quit()

            # Passer le HTML à Scrapy pour parsing
            response = HtmlResponse(url=url, body=page_source, encoding='utf-8')
            yield from self.parse(response)

    def parse(self, response):
        for link in response.css("div#content-container div a::attr(href)").getall():
            yield {'href': f"https://site-catholique.fr{link}"}
