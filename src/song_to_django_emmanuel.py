import mysql.connector
import json
import dotenv
import os, re
import html2text


dotenv.load_dotenv(override=True)


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def html_to_markdown(html_content):
    return html2text.html2text(html_content)

import re

import re

class extract_verses:
    def __init__(self, text: str):
        self.text = text
        self.cut_text(self.text.find('<p>'))
        self.verses = []
        self.verses_txt()


    def verses_txt(self):
        verse_pos = 0
        # print(self.text)
        while self.text.find('<p>') != -1 or self.text.find('<li>') != -1:
            p_pos1 = self.text.find('<p>')
            p_pos2 = self.text.find('</p>')
            li_pos1 = self.text.find('<li>')
            li_pos2 = self.text.find('</li>')
            verse_pos += 1
            if p_pos1 < li_pos1 or li_pos1 == -1:
                pos1 = p_pos1
                pos2 = p_pos2
                plus = 3
            else:
                pos1 = li_pos1
                pos2 = li_pos2
                plus = 4
                
            if pos2 != -1:
                verse = self.text[(pos1 + plus):pos2]
                if verse.find('<strong>') != -1:
                    chorus = True
                else:
                    chorus = None
                verse_clean = re.sub(r'<br\s*/?>', '\n', verse)
                verse_clean = re.sub(r'<.*?>', '', verse_clean)
                verse_clean = re.sub(r'\n+', '\n', verse_clean)
                self.verses.append({'verse_pos': verse_pos, 'verse': chorus, 'text': self.text[:pos2].strip()})
                # print(verse_pos, verse_clean)
            self.cut_text(pos2 + 4)
            # break


    def cut_text(self, pos:int):
        self.text = self.text[pos:].strip()

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

    def select(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    def insert_or_update_song(self, title, description, artist):
        cursor = self.connection.cursor()
        query = '''
INSERT INTO l_songs (title, sub_title, description, artist)
             VALUES (%s, "", %s, %s)
'''
        try:
            cursor.execute(query, (title, description, artist))
            self.connection.commit()
            # print(f"'{title}' updated successfully")
            return 1
        except mysql.connector.Error as error:
            query = '''
UPDATE l_songs
   SET description = %s,
       artist = %s
 WHERE title = %s
'''
            try:
                cursor.execute(query, (description, artist, title))
                self.connection.commit()
                # print(f"'{title}' updated successfully")
                return 2
            except mysql.connector.Error as error:
                print(f"Error >>> {error}")
                return 0
            
    def insert_url(self, title, url):
        cursor = self.connection.cursor()
        query = 'SELECT song_id FROM l_songs WHERE title = %s'
        cursor.execute(query, (title,))
        song_id = cursor.fetchone()
        if song_id:
            query = 'INSERT INTO l_song_link VALUES (%s, %s)'
            try:
                cursor.execute(query, (song_id[0], url))
                self.connection.commit()
            except mysql.connector.Error as error:
                if not 'Duplicate entry' in str(error):
                    print(f"Error >>> {error}")
            
    def insert_genre(self, title, genre):
        cursor = self.connection.cursor()
        query = 'SELECT song_id FROM l_songs WHERE title = %s'
        cursor.execute(query, (title,))
        song_id = cursor.fetchone()
        query = 'SELECT genre_id FROM l_genre WHERE name = %s'
        cursor.execute(query, (genre,))
        genre_id = cursor.fetchone()

        if song_id and genre_id:
            query = 'INSERT INTO l_song_genre VALUES (%s, %s)'
            try:
                cursor.execute(query, (song_id[0], genre_id[0]))
                self.connection.commit()
            except mysql.connector.Error as error:
                if not 'Duplicate entry' in str(error):
                    print(f"Error >>> {error}")
            
    def insert_verse(self, title, num, chorus, text):
        cursor = self.connection.cursor()
        query = 'SELECT song_id FROM l_songs WHERE title = %s'
        cursor.execute(query, (title,))
        song_id = cursor.fetchone()

        if song_id:
            query = 'INSERT INTO l_verses (song_id, num, num_verse, chorus, text) VALUES (%s, %s, %s, %s, %s)'
            try:
                cursor.execute(query, (song_id[0], num, num, chorus, text))
                self.connection.commit()
            except mysql.connector.Error as error:
                if not 'Duplicate entry2' in str(error):
                    print(f"Error >>> {error}")

    def clean(self):
        cursor = self.connection.cursor()

        try:
            query = """
UPDATE l_songs
   SET artist = ''
 WHERE artist LIKE '0%'
    OR artist LIKE '1%'
    OR artist LIKE '2%'
    OR artist LIKE '3%'
    OR artist LIKE '4%'
    OR artist LIKE '5%'
    OR artist LIKE '6%'
    OR artist LIKE '7%'
    OR artist LIKE '8%'
    OR artist LIKE '9%'
 """
            cursor.execute(query)
        except mysql.connector.Error as error:
            print(f"CLEAN 01 - Error >>> {error}")

        try:
            query = """
UPDATE l_songs
   SET artist = ''
 WHERE artist LIKE '%N/A%'
"""
            cursor.execute(query)
        except mysql.connector.Error as error:
            print(f"CLEAN 02 - Error >>> {error}")
        
        try:
            query = """
UPDATE l_songs
   SET description = ''
 WHERE description LIKE '%N/A%'
"""
            cursor.execute(query)
        except mysql.connector.Error as error:
            print(f"CLEAN 03 - Error >>> {error}")

    def close(self):
        if self.connection:
            self.connection.close()    


if __name__ == "__main__":
    db = Database("localhost", os.getenv('DB_LOGIN'), os.getenv('DB_PWD'), "carthographie")
    db.connect()
    
    query = "SELECT * FROM doc_emmanuel"
    results = db.select(query)
    for result in results:
        url = "https://www.emmanuelmusique.com"
        title = result[2]
        category1 = result[3].lower()
        category2 = html_to_markdown(result[4].lower())
        author = "L'Emmanuel"

        db.insert_or_update_song(title.strip(), category2, author)
        db.insert_url(title, url)
        category = category1
        unique_words = set(category)
        for genre in unique_words:
            db.insert_genre(title, genre)

        verses = extract_verses(result[5])
        for verse in verses.verses:
            # print()
            # print(verse)
            if verse['verse']:
                chorus = 0
            else:
                chorus = 1
            db.insert_verse(title, verse['verse_pos'], chorus, verse['text'])
        
        db.clean()
        # break
    
    db.close()