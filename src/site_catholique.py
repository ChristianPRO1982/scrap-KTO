import mysql.connector
from bs4 import BeautifulSoup
import json
import dotenv
import os


dotenv.load_dotenv(override=True)


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def urls(html)->list:
    urls = []

    # Remplacer \" par " si nécessaire
    clean_html = html.replace(r'\"', '"')

    # Parser avec BeautifulSoup
    soup = BeautifulSoup(clean_html, "html.parser")

    # Extraire toutes les URLs des balises <a>
    urls = [a["href"] for a in soup.find_all("a", href=True)]

    # Supprimer les 12 premières valeurs de 'urls'
    urls = urls[12:]

    return urls

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def insert_doc_site_catholique(self, url, type):
        cursor = self.connection.cursor()
        insert_query = "INSERT INTO doc_site_catholique (url, type) VALUES (%s, %s)"
        try:
            cursor.execute(insert_query, (url, type))
            self.connection.commit()
            print(f"URL '{url}' inserted successfully")
            return True
        except mysql.connector.Error as error:
            print(f"Error >>> {error}")
            return False
        cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    file_path = "./output/site_catholique.json"
    data = load_json(file_path)
    
    db = Database("localhost", os.getenv('DB_LOGIN'), os.getenv('DB_PWD'), "carthographie")
    db.connect()

    for item in data:
        virgule = ""

        with open(f'./output/dsc_{item["query_text"]}.json', 'w', encoding='utf-8') as file:
            file.write('[\n')
            for url in urls(item["html"]):
                if db.insert_doc_site_catholique(f"https://site-catholique.fr{url}", f"{item['query_text']}"):
                    file.write(virgule + "{" + f'"url": "https://site-catholique.fr{url}"' + "}")
                    virgule = ",\n"
            file.write('\n]')
        
    db.close()