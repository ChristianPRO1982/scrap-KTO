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

    def insert_or_update(self, url, category, title, content):
        cursor = self.connection.cursor()
        query = "INSERT INTO doc_evangelizo_prayers (url, category, title, content) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE category = %s, title = %s, content = %s"
        try:
            cursor.execute(query, (url, category, title, content, category, title, content))
            self.connection.commit()
            print(f"Term '{title}' updated successfully")
            return True
        except mysql.connector.Error as error:
            print(f"Error >>> {error}")
            return False
        cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    file_path = "./output/Evangelizo_article.json"
    data = load_json(file_path)
    
    db = Database("localhost", "root", os.getenv('DB_PWD'), "carthographie")
    db.connect()
    
    for item in data:
        print(">>>>>", item['title'])
        db.insert_or_update(item['url'], item['category'], item['title'], html_to_markdown(item['content']))
        
    db.close()