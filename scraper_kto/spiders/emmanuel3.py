import scrapy
from urllib.parse import urlparse, parse_qs


genres = {
    1: "Louange",
    2: "Méditation et confiance",
    3: "Enfants",
    33: "Eucharistie",
    6: "Marie",
    7: "Esprit Saint",
    52: "Hymnes et cantiques",
    307: "Messes",
}
def get_genre_name(genre_id):
    return genres.get(genre_id, "Genre inconnu")


class Emmanuel2Spider(scrapy.Spider):
    name = "emmanuel2"
    allowed_domains = ["emmanuelmusic.net"]

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }


    def start_requests(self):
        urls = [
                "https://emmanuelmusic.net/rechercher/?_cat=1",
                # "https://emmanuelmusic.net/rechercher/?_cat=2",
                # "https://emmanuelmusic.net/rechercher/?_cat=3",
                # "https://emmanuelmusic.net/rechercher/?_cat=33",
                # "https://emmanuelmusic.net/rechercher/?_cat=6",
                # "https://emmanuelmusic.net/rechercher/?_cat=7",
                # "https://emmanuelmusic.net/rechercher/?_cat=52",
                # "https://emmanuelmusic.net/rechercher/?_cat=307",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        h2s = response.css("h2")
        parsed_url = urlparse(response.url)
        cat_value = parse_qs(parsed_url.query).get('_cat', [None])[0]

        for h2 in h2s:
            href = h2.css("a::attr(href)").get()
            langue = h2.css("span").get()
            if "fi-fr" in langue or "fi-en" in langue:
                yield {
                    "genre": get_genre_name(int(cat_value)),
                    "langue": langue,
                    "href": href
                }
                # yield response.follow(
                #     href,
                #     callback=self.parse_chant,
                #     meta={"genre": get_genre_name(int(cat_value))},
                # )
                break;


    def parse_chant(self, response):
        title = response.css("h4::text").get()
        genre = response.meta.get("genre")
        div_info = response.css("div.elementor-heading-title.elementor-size-medium").get()
        div_p = div_info.split("<p>")[1].split("</p>")[0]
        div1 = response.css("div.elementor-widget-woocommerce-product-content").get()
        # div2 = div1.css("dev::text").get()
        
        # div_chant = div.css("div.chant-contenu")
        # ps = div_chant.css("p")
        # lyrics = ""
        # for p in ps:
        #     lyrics += p.get()

        yield {
            "title": title.strip() if title else "N/A",
            "url": response.url,
            "genre": genre,
            "info": div_p.strip() if div_p else "N/A",
            # "category1": category1.strip() if category1 else "N/A",
            # "category2": category2.strip() if category2 else "N/A",
            "lyrics": div1.strip() if div1 else "N/A",
        }