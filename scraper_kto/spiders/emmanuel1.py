import scrapy


class Emmanuel1Spider(scrapy.Spider):
    name = "emmanuel1"
    allowed_domains = ["catechisme-emmanuel.com"]
    start_urls = ["https://catechisme-emmanuel.com/tous-les-chants/"]

    def parse(self, response):
        divs = response.css("div.cat-wrap.shadow-1")

        for div in divs:
            h5 = div.css("h5::text").get()
            ul = div.css("ul.cat-list")
            for li in ul.css("li"):
                href = li.css("a::attr(href)").get()
                yield response.follow(
                    href,
                    callback=self.parse_chant,
                    meta={"category1": h5},
                )
                # break
    
    def parse_chant(self, response):
        category1 = response.meta.get("category1")
        
        div = response.css("div.entry-content")
        category2 = response.css("em::text").get()
        title = response.css("h2::text").get()
        div_chant = div.css("div.chant-contenu")
        ps = div_chant.css("p")
        lyrics = ""
        for p in ps:
            lyrics += p.get()

        yield {
            "title": title.strip() if title else "N/A",
            "url": response.url,
            "category1": category1.strip() if category1 else "N/A",
            "category2": category2.strip() if category2 else "N/A",
            "lyrics": lyrics.strip() if lyrics else "N/A",
        }