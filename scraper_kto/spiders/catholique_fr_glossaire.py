import scrapy


class CatholiqueFrGlossaireSpider(scrapy.Spider):
    name = "catholique_fr_glossaire"
    allowed_domains = ["eglise.catholique.fr"]
    start_urls = ["https://eglise.catholique.fr/glossaire/"]

    def parse(self, response):
        """Scrape la page principale du glossaire et suit chaque lien trouvé"""
        ols = response.css('ol.bloc-index-list-letter')

        for ol in ols:
            for li in ol.css('li'):
                href = li.css('a::attr(href)').get()
                term = li.css('a::text').get()

                if href:
                    url = response.urljoin(href)
                    yield scrapy.Request(
                        url,
                        callback=self.parse_letter_page,
                        meta={"term": term, "url": url},  # On passe les données
                    )

    def parse_letter_page(self, response):
        """Scrape la page cible d'un terme du glossaire"""
        
        ols = response.css('ol.bloc-index-list')

        for ol in ols:
            for li in ol.css('li'):
                href = li.css('a::attr(href)').get()
                term = li.css('a::text').get()

                if href:
                    url = response.urljoin(href)
                    yield scrapy.Request(
                        url,
                        callback=self.parse_page,
                        meta={"term": term, "url": url},  # On passe les données
                    )

    def parse_page(self, response):
        """Scrape la page cible d'un terme du glossaire"""
        div = response.css('div.spotlight02').get()

        yield {
            "url": response.meta["url"],
            "term": response.meta["term"],
            "definition": div,
        }