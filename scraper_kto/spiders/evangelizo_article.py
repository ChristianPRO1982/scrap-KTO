import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
import time
import json


class EvangelizoArticleSpider(scrapy.Spider):
    name = "evangelizo_article"
    allowed_domains = ["levangileauquotidien.org"]
    start_urls = ["https://levangileauquotidien.org/FR/"]
    dotjsons = [
        "Evangelizo"
    ]

    def __init__(self):
        options = Options()
        # options.add_argument("--headless")  # Activer pour exécution sans affichage
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def start_requests(self):
        for dotjson in self.dotjsons:
            with open(f"./output/{dotjson}.json") as json_file:
                data = json.load(json_file)
            
            for item in data:
                yield scrapy.Request(
                    url=item['url'],
                    callback=self.parse,
                    meta={'category': item['category'], 'url': item['url']}
                )
                # break

    def parse(self, response):
        self.driver.get(response.url)
        wait = WebDriverWait(self.driver, 10)

        try:
            # Attendre que la page soit chargée
            time.sleep(2)  # Attente supplémentaire pour être sûr que le contenu est bien rendu

            # Récupérer le HTML mis à jour après le chargement
            html = self.driver.page_source
            sel = Selector(text=html)

            # Extraire les informations demandées
            title = sel.css("h1.title-main.font-2::text").get()
            content = sel.css("article.PrayerDetail.content.prayer-detail").get()

            yield {
                "url": response.url,
                "category": response.meta["category"],
                "title": title.strip() if title else "N/A",
                "content": content.strip() if content else "N/A",
            }

        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la page détail : {e}")
            yield {
                "url": response.url,
                "category": response.meta["category"],
                "title": "N/A",
                "content": "N/A",
            }

    def closed(self, reason):
        self.driver.quit()  # Fermer le navigateur Selenium
