import scrapy


class Chant2Spider(scrapy.Spider):
    name = "chant2"
    allowed_domains = ["choralepolefontainebleau.org"]
    start_urls = [
        "https://choralepolefontainebleau.org/category/bibliotheque/messes/",
        "https://choralepolefontainebleau.org/category/bibliotheque/psaumes/",
        "https://choralepolefontainebleau.org/category/bibliotheque/hymnes-liturgie-des-heures/",
        "https://choralepolefontainebleau.org/category/bibliotheque/missel-romain/",
        "https://choralepolefontainebleau.org/category/bibliotheque/cantiques/",
        "https://choralepolefontainebleau.org/category/bibliotheque/registre-latin/",
        "https://choralepolefontainebleau.org/category/bibliotheque/repertoire-aumonerie/",
        "https://choralepolefontainebleau.org/category/bibliotheque/repertoire-gospel/",
        "https://choralepolefontainebleau.org/category/bibliotheque/repertoire-anglais/",
    ]

    def parse(self, response):
        category1 = response.css("h1.page-title::text").get()

        h5s = response.css("h5")
        for h5 in h5s:
            href = h5.css("a::attr(href)").get()
            title = h5.css("a::text").get()

            yield response.follow(
                href,
                callback=self.parse_chant,
                meta={"title": title, "category1": category1, "category2": None, "author": None},
                )
            # break
    
    def parse_chant(self, response):
        title = response.meta.get("title")
        category1 = response.meta.get("category1")
        category2 = response.meta.get("category2")
        author = response.meta.get("author")

        h4 = response.css("h4::text").get()
        p = response.css("ul li span p").get()
        
        lyrics = response.css("div.paroles").get()
        if not lyrics:
            paroles_div = response.xpath("//div[h3[text()='Paroles :']]").get()
            if paroles_div:
                lyrics = paroles_div

        yield {
            "title": title.strip() if title else "N/A",
            "url": response.url,
            "category1": category1.strip() if category1 else "N/A",
            "category2": category2.strip() if category2 else "N/A",
            "author": author.strip() if author else "N/A",
            "reference": h4.strip() + "\n\n" + p.strip() if h4 and p else "N/A",
            "lyrics": lyrics.strip() if lyrics else "N/A",
        }
