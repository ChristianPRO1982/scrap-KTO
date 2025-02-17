import scrapy
from scraper_kto.spiders.utils import common_headers


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
        for url in self.start_urls:
            yield scrapy.Request(url, headers=common_headers)
    

    def parse(self, response):
        print(">>>>>", response.url)