import mysql.connector
import json
import dotenv
import os
import html2text


dotenv.load_dotenv(override=True)


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def html_to_markdown(html_content):
    return html2text.html2text(html_content)

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

    def update(self, url, content):
        cursor = self.connection.cursor()
        query = "UPDATE doc_site_catholique SET text = %s WHERE url = %s"
        try:
            cursor.execute(query, (content, url))
            self.connection.commit()
            # print(f"URL '{url}' updated successfully")
            return True
        except mysql.connector.Error as error:
            print(f"Error >>> {error} / url: {url}")
            return False
        cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    file_path = "./output/site_catholique_article.json"
    data = load_json(file_path)
    
    db = Database("localhost", os.getenv('DB_LOGIN'), os.getenv('DB_PWD'), "carthographie")
    db.connect()
    
    for item in data:

        db.update((item["url"]), html_to_markdown(item["content"]))
        
    db.close()