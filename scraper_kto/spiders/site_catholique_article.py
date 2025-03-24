import scrapy
import json


class SiteCatholiqueArticleSpider(scrapy.Spider):
    name = "site_catholique_article"
    allowed_domains = ["site-catholique.fr"]
    start_urls = [
        "https://site-catholique.fr/"
    ]
    dotjsons = [
        "Chapelets",
        "Chemins-de-Croix",
        "Humour",
        "Prieres",
        "Sacrements"
    ]

    def start_requests(self):
        for dotjson in self.dotjsons:
            with open(f"./output/dsc_{dotjson}.json") as json_file:
                data = json.load(json_file)
            
            for item in data:
                yield scrapy.Request(
                    url=item['url'],
                    callback=self.parse,
                    meta={'topic': dotjson}
                )

    def parse(self, response):
        divs = response.css('div[style*="background:#efefef;"]')
        if len(divs) == 1:
            div = divs[0]
            yield {
                'topic': response.meta['topic'],
                'div_count': len(divs),
                'content': div.get()
            }