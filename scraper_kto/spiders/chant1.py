import scrapy


class Chant1Spider(scrapy.Spider):
    name = "chant1"
    allowed_domains = ["choralepolefontainebleau.org"]
    start_urls = [
        # "https://choralepolefontainebleau.org/category/bibliotheque/chants/",
        # "https://choralepolefontainebleau.org/category/bibliotheque/chants-de-louanges/",
        "https://choralepolefontainebleau.org/category/bibliotheque/repertoire-enfants/",
    ]

    def parse(self, response):
        category1 = response.css("h1::text").get()  # Récupère le titre principal de la page

        # Vérifie si <tbody> existe
        tbody = response.css("tbody")
        if not tbody:
            self.logger.warning("Aucun <tbody> trouvé sur cette page : %s", response.url)
            return  # Arrête l'exécution de parse si aucun tbody n'est trouvé

        # ✅ Utilisation correcte de `for tr in tbody.css("tr")`
        for tr in tbody.css("tr"):  
            tds = tr.css("td")  # ✅ Ne pas faire `.getall()`, on garde le sélecteur Scrapy
            if len(tds) < 3:
                continue  # S'assure qu'il y a bien 3 <td>

            href = tds[0].css("a::attr(href)").get()
            title = tds[0].css("a::text").get()
            category2 = tds[1].css("::text").get()
            author = tds[2].css("::text").get()

            yield response.follow(
                href,
                callback=self.parse_chant,
                meta={"title": title, "category1": category1, "category2": category2, "author": author},
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
