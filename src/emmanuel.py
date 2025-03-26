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

    def insert_or_update(self, url, title, category1, category2, lyrics_html, lyrics_md):
        cursor = self.connection.cursor()
        query = """
INSERT INTO doc_emmanuel (url,
                          title,
                          category1,
                          category2,
                          lyrics_html,
                          lyrics_md)
                  VALUES (%s, %s, %s, %s, %s, %s)
"""
        try:
            cursor.execute(query, (url, title, category1, category2, lyrics_html, lyrics_md))
            self.connection.commit()
            # print(f"'{title}' updated successfully")
            return 1
        except mysql.connector.Error as error:
            query = """
UPDATE doc_emmanuel
   SET title = %s,
       category1 = %s,
       category2 = %s,
       lyrics_html = %s,
       lyrics_md = %s
 WHERE url = %s
"""
            try:
                cursor.execute(query, (title, category1, category2, lyrics_html, lyrics_md, url))
                self.connection.commit()
                return 2
            except mysql.connector.Error as error:
                print(f"Error >>> {error}")
                return 0
        cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()    


if __name__ == "__main__":
    file_path = [
        "./output/emmanuel1.json"
        ]
    
    db = Database("localhost", "root", os.getenv('DB_PWD'), "carthographie")
    db.connect()
    
    i1 = 0
    i2 = 0
    for file in file_path:
        data = load_json(file)
        for item in data:
            action = db.insert_or_update(
                item['url'],
                item['title'],
                item['category1'],
                item['category2'],
                item['lyrics'],
                html_to_markdown(item['lyrics']))
            if action == 1:
                i1 += 1
            elif action == 2:
                i2 += 1
                # print(">>>>>", item['title'])
    
    print(f"Total inserted: {i1}")
    print(f"Total updated: {i2}")
    db.close()