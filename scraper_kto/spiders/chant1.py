import scrapy


class Chant1Spider(scrapy.Spider):
    name = "chant1"
    allowed_domains = ["choralepolefontainebleau.org"]
    start_urls = ["https://choralepolefontainebleau.org/"]

    def parse(self, response):
        pass
