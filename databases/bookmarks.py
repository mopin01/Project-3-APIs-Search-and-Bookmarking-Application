import sqlite3
import threading
import os


class Bookmarks:
    # Define columns for the database table
    columns = ['title', 'overview', 'release_date', 'id', 'original_title']

    def __init__(self):
        # Create a thread-local variable to hold a separate database connection for each thread
        self.conn_per_thread = threading.local()

        # Connect to the database
        try:
            self.conn = sqlite3.connect(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "bookmarks.db"
                ),
                check_same_thread=False  # Allow connections from multiple threads
            )
        except sqlite3.Error as e:
            # print(f"Error connecting to cache database: {e}")
            raise e

        # Create a cursor object to execute SQL commands
        self.cur = self.conn.cursor()

        # Create the table if it doesn't exist already
        self.create_table()

    def create_table(self):
        # Create the movies table if it doesn't exist already
        try:
            columns_sql = ','.join(f"{col} TEXT" for col in self.columns)
            self.cur.execute(
                f"CREATE TABLE IF NOT EXISTS movies ({columns_sql}, PRIMARY KEY (title))"
            )
        except sqlite3.Error as e:
            # print(f"Error creating movies table: {e}")
            raise e

    def add_movie(self, data):
        # Get the database connection for this thread
        conn = self._get_conn()

        # Build the SQL query
        columns_sql = ','.join(self.columns)
        placeholders_sql = ','.join(['?' for _ in range(len(self.columns))])
        values = [data.get(col, None) for col in self.columns]

        try:
            # Try to insert the data into the table
            with conn:
                conn.execute(
                    f"INSERT INTO movies ({columns_sql}) VALUES ({placeholders_sql})",
                    values
                )
        except sqlite3.IntegrityError as e:
            # If the movie already exists in the table, update its data instead
            if "UNIQUE constraint failed" in str(e):
                # print("Movie already exists in the database.")
                with conn:
                    update_sql = f"UPDATE movies SET overview=?, release_date=?, id=?, original_title=? WHERE title=?"
                    update_values = [data.get('overview', None), data.get('release_date', None), data.get('id', None), data.get('original_title', None), data['title']]
                    conn.execute(update_sql, update_values)
            else:
                # If there's another error, raise an exception
                # print(f"Error adding movie to database: {e}")
                raise e
        except sqlite3.Error as e:
            # If there's another error, raise an exception
            # print(f"Error adding movie to database: {e}")
            raise e


    def get_movie(self, title):
        # Get the database connection for this thread
        conn = self._get_conn()

        # Retrieve the movie data from the table
        with conn:
            try:
                self.cur.execute("SELECT * FROM movies WHERE title=?", (title,))
                row = self.cur.fetchone()
                if row is None:
                    return None
                return dict(zip(self.columns, row))
            except sqlite3.Error as e:
                # If there's an error, raise an exception
                # print(f"Error retrieving movie from database: {e}")
                raise e
    
    def delete_movie(self, title):
        # Get a connection to the database
        conn = self._get_conn()
        # Use a "with" block to ensure the connection is properly closed when done
        with conn:
            # Check if the movie exists in the database
            cursor = conn.execute("SELECT COUNT(*) FROM movies WHERE title=?", (title,))
            count = cursor.fetchone()[0]
            if count == 0:
                # If the movie doesn't exist, raise a ValueError
                raise ValueError(f"Movie '{title}' not found in database.")
            else:
                # If the movie exists, delete it from the database
                conn.execute("DELETE FROM movies WHERE title=?", (title,))
                # print(f"Movie '{title}' deleted from database.")


    def get_all_movies(self):
        # Get a connection to the database
        conn = self._get_conn()
        # Use a "with" block to ensure the connection is properly closed when done
        with conn:
            try:
                # Execute a SELECT statement to retrieve all movies from the database
                self.cur.execute("SELECT * FROM movies")
                rows = self.cur.fetchall()
                results = []
                # Convert the rows to a list of dictionaries (one dictionary per movie)
                for row in rows:
                    results.append(dict(zip(self.columns, row)))
                # Return the list of movies
                return results
            except sqlite3.Error as e:
                # If an error occurs during retrieval, print an error message and raise the error
                # print(f"Error retrieving bookmarks from database: {e}")
                raise e
    
    def clear_database(self):
        # Get a connection to the database
        conn = self._get_conn()
        # Use a "with" block to ensure the connection is properly closed when done
        with conn:
            try:
                # Execute a DELETE statement to remove all rows from the movies table
                conn.execute("DELETE FROM movies")
                # print("All data cleared from movies table.")
            except sqlite3.Error as e:
                # If an error occurs during deletion, print an error message and raise the error
                # print(f"Error clearing data from movies table: {e}")
                raise e

    def _get_conn(self):
        # If a connection for this thread doesn't already exist, create one
        if not hasattr(self.conn_per_thread, "conn"):
            try:
                self.conn_per_thread.conn = sqlite3.connect(
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "bookmarks.db"
                    ),
                    # Disable thread checking for SQLite connections
                    check_same_thread=False
                )
            except sqlite3.Error as e:
                # If an error occurs during connection creation, print an error message and raise the error
                # print(f"Error connecting to cache database: {e}")
                raise e
        # Return the existing connection
        return self.conn_per_thread.conn