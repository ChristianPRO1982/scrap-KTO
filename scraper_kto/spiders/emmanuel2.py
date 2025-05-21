import scrapy


class Emmanuel2Spider(scrapy.Spider):
    name = "emmanuel2"
    allowed_domains = ["emmanuelmusic.net"]
    start_urls = ["https://emmanuelmusic.net"]

    def parse(self, response):
        pass
