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

    def insert_or_update(self, url, title, category1, category2, author, reference, lyrics_html, lyrics_md):
        cursor = self.connection.cursor()
        query = "INSERT INTO doc_choralepolefontainebleau (url, title, category1, category2, author, reference, lyrics_html) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = %s, category1 = %s, category2 = %s, author = %s, reference = %s, lyrics_html = %s, lyrics_md = %s"
        try:
            cursor.execute(query, (url, title, category1, category2, author, reference, lyrics_html, lyrics_md, title, category1, category2, author, reference, lyrics_html, lyrics_md))
            self.connection.commit()
            print(f"'{title}' updated successfully")
            return True
        except mysql.connector.Error as error:
            print(f"Error >>> {error}")
            return False
        cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()    


if __name__ == "__main__":
    file_path = [
        "./output/chant1-1.json",
        "./output/chant1-2.json",
        "./output/chant1-3.json",
        "./output/chant2-1.json"
        ]
    
    db = Database("localhost", "root", os.getenv('DB_PWD'), "carthographie")
    db.connect()
    
    for file in file_path:
        data = load_json(file)
        for item in data:
            print(">>>>>", item['title'])
            db.insert_or_update(
                item['url'],
                item['title'],
                item['category1'],
                item['category2'],
                item['author'],
                item['reference'],
                item['lyrics'],
                html_to_markdown(item['lyrics']))
        
    db.close()