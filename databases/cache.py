import sqlite3
import threading
import os

class Cache:

    def __init__(self):
        self.conn_per_thread = threading.local()
        
        try:
            self.conn = sqlite3.connect(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'cache.db'
                ),
                check_same_thread=False
            )
        except sqlite3.Error as e:
            raise e
        self.cur = self.conn.cursor()
        # Clear cache on startup
        self.clear_cache()


    def create_table(self, data):
        conn = self._get_conn()
        with conn:
            try:
                # Create table with collumns determined by the data being fed
                column_names = ", ".join(key for key in data.keys())
                self.cur.execute(f'CREATE TABLE IF NOT EXISTS movies ({column_names})')

                # Add initial movie
                columns = ', '.join(data.keys())
                values = ', '.join(['?'] * len(data))
                self.cur.execute(f'INSERT INTO movies ({columns}) VALUES ({values})', list(data.values()))
            except sqlite3.Error as e:
                raise e


    def add_movie(self, data):
        conn = self._get_conn()
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
                        self.cur.execute(f'INSERT INTO movies ({columns}) VALUES ({values})', list(data.values()))
                else:
                    # Create table if doesn't exist
                    self.create_table(data)
            except sqlite3.Error as e:
                raise e


    def get_movie(self, title):
        conn = self._get_conn()
        with conn:
            try:
                self.cur.execute('SELECT * FROM movies WHERE title=?', (title,))
                row = self.cur.fetchone()
                columns = [col[0] for col in self.cur.description]
                data = dict(zip(columns, row))
                return data
            except sqlite3.Error as e:
                raise e
    

    def movie_exists(self, title):
        conn = self._get_conn()
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
        conn = self._get_conn()
        with conn:
            try:
                self.cur.execute('DROP TABLE IF EXISTS movies')
            except sqlite3.Error as e:
                raise e


    def _get_conn(self):
        # Get the database connection for the current thread
        if not hasattr(self.conn_per_thread, 'conn'):
            try:
                self.conn_per_thread.conn = sqlite3.connect(
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'cache.db'
                    ),
                    check_same_thread=False  # Allow connections from multiple threads
                )
            except sqlite3.Error as e:
                raise e
        return self.conn_per_thread.conn