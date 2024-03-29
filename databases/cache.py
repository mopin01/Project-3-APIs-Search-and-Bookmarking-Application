import sqlite3
import threading
import os

class Cache:

    def __init__(self, db_name='cache.db'):
        self.conn_per_thread = threading.local()
        self.db_name = db_name
        try:
            self.conn = sqlite3.connect(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    self.db_name),
                check_same_thread=False
            )
        except sqlite3.Error as e:
            raise e
        
        self.cur = self.conn.cursor()
        # Clear cache on startup
        self.clear_cache()


    def create_table(self, data):
        conn = self.conn
        with conn:
            try:
                # Create table with collumns determined by the data being fed
                column_names = ", ".join(key for key in data.keys())
                conn.execute(f'CREATE TABLE IF NOT EXISTS movies ({column_names})')

                # Add initial movie
                columns = ', '.join(data.keys())
                values = ', '.join(['?'] * len(data))
                conn.execute(f'INSERT INTO movies ({columns}) VALUES ({values})', list(data.values()))
            except sqlite3.Error as e:
                raise e


    def add_movie(self, data):
        conn = self.conn
        with conn:
            try:
                # Check if table exists
                self.cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="movies"')
                if self.cur.fetchone() is not None:
                    # Check if movie already exists
                    self.cur.execute('SELECT * FROM movies WHERE title=?', (data.get('title'),))
                    if self.cur.fetchone() is None:
                        # Insert movie
                        columns = ', '.join(data.keys())
                        values = ', '.join(['?'] * len(data))
                        conn.execute(f'INSERT INTO movies ({columns}) VALUES ({values})', list(data.values()))
                else:
                    # Create table if doesn't exist
                    self.create_table(data)
            except sqlite3.Error as e:
                raise e


    def get_movie_by_title(self, title):
        conn = self.conn
        with conn:
            try:
                if self.movie_exists(title):
                    self.cur.execute('SELECT * FROM movies WHERE title=?', (title,))
                    row = self.cur.fetchone()
                    columns = [col[0] for col in self.cur.description]
                    data = dict(zip(columns, row))
                    return data
                else:
                    raise ValueError(f"Movie with title '{title}' not found")
            except sqlite3.Error as e:
                raise e
    

    def get_all_titles(self):
        conn = self.conn
        with conn:
            try:
                self.cur.execute('SELECT title FROM movies')
                titles = self.cur.fetchall()
                return [title[0].replace("'", "").replace("(", "").replace(")", "") for title in titles]
            except sqlite3.Error as e:
                raise e
    

    def movie_exists(self, title):
        conn = self.conn
        with conn:
            try:
                self.cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="movies"')
                if self.cur.fetchone() is None:
                    return False
                
                self.cur.execute("SELECT * FROM movies WHERE title = ?", (title,))
                result = self.cur.fetchone()
                if result is not None:
                    return True
                else:
                    return False
            except sqlite3.Error as e:
                raise e


    def clear_cache(self):
        # Clear all data from the 'movies' table
        conn = self.conn
        with conn:
            try:
                self.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='movies'")
                if self.cur.fetchone():
                    conn.execute('DELETE FROM movies')
            except sqlite3.Error as e:
                raise e
    
    
    def delete_table(self):
        conn = self.conn
        with conn:
            try:
                conn.execute('DROP TABLE IF EXISTS movies')
            except sqlite3.Error as e:
                raise e