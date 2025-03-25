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


class EvangelizoSpider(scrapy.Spider):
    name = "evangelizo"
    allowed_domains = ["levangileauquotidien.org"]
    start_urls = ["https://levangileauquotidien.org/FR/prayer"]

    def __init__(self):
        options = Options()
        # options.add_argument("--headless")  # Activer pour exécution sans affichage
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def parse(self, response):
        self.driver.get(response.url)
        wait = WebDriverWait(self.driver, 2)

        # Récupérer les balises <p> qui doivent être cliquées
        prayer_titles = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.PrayerCategory-title.item-title"))
        )

        for title in prayer_titles:
            try:
                # Cliquer sur la balise <p> pour révéler le <ul>
                self.driver.execute_script("arguments[0].click();", title)
                title_text = title.text
                
                # Attendre que le <ul> apparaisse après le clic
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul"))
                )

                # Récupérer le HTML mis à jour
                html = self.driver.page_source
                sel = Selector(text=html)

                # Extraire les URLs des balises <a> à l'intérieur des <ul>
                links = sel.css("ul a.PrayerCategory-link::attr(href)").getall()
                for link in links:
                    absolute_url = response.urljoin(link)
                    yield {
                        "category": title_text,
                        "url": absolute_url,
                    }
                    # yield scrapy.Request(absolute_url, callback=self.parse_detail, meta={"category": title_text})

            except Exception as e:
                self.logger.error(f"Erreur lors du clic sur un élément : {e}")

    def parse_detail(self, response):
        """Ouvre chaque page de détail avec Selenium et extrait les données."""
        self.driver.get(response.url)
        wait = WebDriverWait(self.driver, 2)

        try:
            # Attendre que la page soit chargée
            time.sleep(3)  # Attente supplémentaire pour être sûr que le contenu est bien rendu

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
