import scrapy


class Chant2Spider(scrapy.Spider):
    name = "chant2"
    allowed_domains = ["choralepolefontainebleau.org"]
    start_urls = ["https://choralepolefontainebleau.org/"]

    def parse(self, response):
        pass
