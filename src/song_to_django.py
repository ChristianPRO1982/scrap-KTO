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

class extract_verses:
    def __init__(self, text: str):
        self.text = text
        self.verses = []
        self.verses_txt()

    def verses_txt(self):
        verse_pos = 0
        while self.text.find('**') != -1:
            verse_pos += 1
            num, pos1, pos2 = self.num_verse()
            if num:
                self.cut_text(pos1)
                if pos1 < pos2:
                    self.verses.append({'verse_pos': verse_pos, 'verse': num, 'text': self.text[:pos2].strip()})
                else:
                    self.verses.append({'verse_pos': verse_pos, 'verse': num, 'text': self.text.strip()})
                self.cut_text(pos2)
                # print("verse")
            else:
                self.verses.append({'verse_pos': verse_pos, 'verse': num, 'text': self.extract_chorus()})
                # print("chorus")
            
            if verse_pos > 1000:
                print("break")
                break
        
        if verse_pos == 0:
            self.verses.append({'verse_pos': verse_pos, 'verse': 1, 'text': self.text})

    def num_verse(self)->tuple:
        pos = self.text.find('**')
        pos1 = self.text.find('**', pos + 2) + 2
        pos2 = self.text.find('**', pos1 + 2 + 2)
        num_txt = self.text[(pos + 2):(pos+6)]
        try:
            num = int(num_txt.strip('*. -'))
        except:
            num = None
        return num, pos1, pos2 - pos1 - 1
    
    def extract_chorus(self)->str:
        pos1 = self.text.find('**')
        pos2 = self.text.find('**', pos1 + 2) + 2
        if pos1 < pos2:
            chorus = self.text[pos1+2:pos2-2].strip()
        else:
            chorus = self.text[pos1+2:].strip()
        self.cut_text(pos2)
        return chorus
    
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
    
    query = "SELECT * FROM doc_choralepolefontainebleau"
    results = db.select(query)
    for result in results:
        url = result[1]
        title = result[2]
        category1 = result[3].lower()
        category2 = result[4].lower()
        author = result[5]
        reference = html_to_markdown(result[6])

        db.insert_or_update_song(title.strip(), reference.strip(), author)
        db.insert_url(title, url)
        category = category1 + " " + category2
        category = category.lower().split()
        unique_words = set(category)
        for genre in unique_words:
            db.insert_genre(title, genre)

        verses = extract_verses(result[8])
        for verse in verses.verses:
            # print()
            # print(verse)
            if verse['verse']:
                chorus = 0
            else:
                chorus = 1
            db.insert_verse(title, verse['verse_pos'], chorus, verse['text'])
        
        # break
    
    db.clean()
    db.close()