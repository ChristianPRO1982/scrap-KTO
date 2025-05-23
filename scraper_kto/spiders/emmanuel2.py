import scrapy


class Emmanuel2Spider(scrapy.Spider):
    name = "emmanuel2"
    allowed_domains = ["emmanuelmusic.net"]
    # start_urls = [
    #     "https://emmanuelmusic.net/rechercher/?_cat=1",
    #     "https://emmanuelmusic.net/rechercher/?_cat=2",
    #     "https://emmanuelmusic.net/rechercher/?_cat=3",
    #     "https://emmanuelmusic.net/rechercher/?_cat=33",
    #     "https://emmanuelmusic.net/rechercher/?_cat=6",
    #     "https://emmanuelmusic.net/rechercher/?_cat=7",
    #     "https://emmanuelmusic.net/rechercher/?_cat=52",
    #     "https://emmanuelmusic.net/rechercher/?_cat=307",
    #     ]
    Louange
    Méditation et confiance
    Enfants
    Eucharistie
    Marie
    Esprit Saint
    Hymnes et cantiques
    Messes

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }


    def start_requests(self):
        urls = [
                # "https://emmanuelmusic.net/rechercher/?_cat=1",
                # "https://emmanuelmusic.net/rechercher/?_cat=2",
                # "https://emmanuelmusic.net/rechercher/?_cat=3",
                "https://emmanuelmusic.net/rechercher/?_cat=33",
                # "https://emmanuelmusic.net/rechercher/?_cat=6",
                # "https://emmanuelmusic.net/rechercher/?_cat=7",
                # "https://emmanuelmusic.net/rechercher/?_cat=52",
                # "https://emmanuelmusic.net/rechercher/?_cat=307",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        h2s = response.css("h2")

        for h2 in h2s:
            href = h2.css("a::attr(href)").get()
            h2_text = h2.css("::text").get()
            
            yield {
                "h2_text": h2_text.strip() if h2_text else None,
                "href": href
            }
            # yield response.follow(
            #     href,
            #     callback=self.parse_chant,
            #     meta={"category1": h5},
            # )
            break;


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