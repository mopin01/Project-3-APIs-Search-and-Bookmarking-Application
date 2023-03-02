import sqlite3
import threading
import os

class Cache:
    # Define columns for the database table
    columns = ['title', 'overview', 'release_date', 'id', 'original_title']

    def __init__(self):
        # Create a separate database connection for each thread
        self.conn_per_thread = threading.local()
        
        # Connect to the cache database and create a cursor
        try:
            self.conn = sqlite3.connect(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "cache.db"
                ),
                check_same_thread=False  # Allow connections from multiple threads
            )
        except sqlite3.Error as e:
            print(f"Error connecting to cache database: {e}")
            raise e
        self.cur = self.conn.cursor()

        # Create the 'movies' table in the database
        self.create_table()

    def create_table(self):
        # Drop the 'movies' table if it already exists
        try:
            self.cur.execute("DROP TABLE IF EXISTS movies")
            # Create a new 'movies' table with columns as defined in self.columns
            columns_sql = ','.join(f"{col} TEXT" for col in self.columns)
            self.cur.execute(
                f"CREATE TABLE movies ({columns_sql}, PRIMARY KEY (title))"
            )
        except sqlite3.Error as e:
            print(f"Error creating movies table: {e}")
            raise e

    def add_movie(self, data):
        # Add a movie to the 'movies' table
        conn = self._get_conn()
        columns_sql = ','.join(self.columns)
        placeholders_sql = ','.join(['?' for _ in range(len(self.columns))])
        values = [data.get(col, None) for col in self.columns]
        try:
            with conn:
                conn.execute(
                    f"INSERT INTO movies ({columns_sql}) VALUES ({placeholders_sql})",
                    values
                )
        except sqlite3.Error as e:
            print(f"Error adding movie to database: {e}")
            raise e

    def get_movie(self, title):
        # Retrieve a movie from the 'movies' table using its title
        conn = self._get_conn()
        with conn:
            try:
                self.cur.execute("SELECT * FROM movies WHERE title=?", (title,))
                row = self.cur.fetchone()
                if row is None:
                    return None
                # Return a dictionary with column names as keys and row values as values
                return dict(zip(self.columns, row))
            except sqlite3.Error as e:
                print(f"Error retrieving movie from database: {e}")
                raise e

    def _get_conn(self):
        # Get the database connection for the current thread
        if not hasattr(self.conn_per_thread, "conn"):
            try:
                self.conn_per_thread.conn = sqlite3.connect(
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "cache.db"
                    ),
                    check_same_thread=False  # Allow connections from multiple threads
                )
            except sqlite3.Error as e:
                print(f"Error connecting to cache database: {e}")
                raise e
        return self.conn_per_thread.conn
