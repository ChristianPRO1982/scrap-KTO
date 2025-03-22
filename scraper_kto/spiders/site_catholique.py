import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from scraper_kto.spiders.utils import common_headers
from selenium import webdriver
from scrapy.http import HtmlResponse





class SiteCatholiqueSpider(scrapy.Spider):
    name = "site_catholique"
    allowed_domains = ["site-catholique.fr"]
    start_urls = [
        "https://site-catholique.fr/?Prieres",
        # "https://site-catholique.fr/?Chapelets",
        # "https://site-catholique.fr/?Chemins-de-Croix",
        # "https://site-catholique.fr/?Sacrements",
        # "https://site-catholique.fr/?Humour",
        ]


    def start_requests(self):
        for url in self.start_urls:
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            
            # Scroll
            for _ in range(0):
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                time.sleep(3)  # Laisse le temps au site de charger les éléments

            # Une fois la page scrollée, récupère l'HTML de la page
            page_source = driver.page_source

            # Crée une réponse Scrapy avec l'HTML chargé par Selenium
            response = HtmlResponse(url=url, body=page_source, encoding='utf-8')
            
            # Passe la réponse au parseur Scrapy
            yield self.parse(response)

            driver.quit()

    def parse(self, response):
        # Cette fonction est appelée une fois que la page a été chargée et scrollée
        # Utilisation de Scrapy pour parser le HTML
        content_container = response.css("div#content-container")  # Utilisation de la méthode Scrapy pour rechercher l'élément
        
        divs = content_container.css("div")  # Trouve tous les divs dans ce conteneur
        for div in divs:
            href = div.css("a::attr(href)").get()  # Extrait l'attribut href de chaque lien
            if href:
                yield {'href': href}  # Renvoie les href extraits