import sqlite3

conn = sqlite3.connect('database/database.db')

cursor = conn.cursor()

# (Temporary) List to edit database collumns
table_columns = [
    {'name': 'title', 'type': 'TEXT'},
    {'name': 'director', 'type': 'TEXT'},
    {'name': 'year_published', 'type': 'INTEGER'}
]

def create_table():
    column_str = ", ".join([f"{col['name']} {col['type']}" for col in table_columns])
    
    cursor.execute(f"DROP TABLE IF EXISTS movies")
    cursor.execute(f"CREATE TABLE movies ({column_str})")
    conn.commit()

def add_movie(data):
    column_names = ", ".join([col['name'] for col in table_columns])
    placeholders = ", ".join(["?" for col in table_columns])
    
    values = [data[col['name']] for col in table_columns]
    cursor.execute(f"INSERT INTO movies ({column_names}) VALUES ({placeholders})", values)
    conn.commit()

def edit_movie(title, new_data):
    set_str = ", ".join([f"{col['name']}=?" for col in table_columns])
    
    values = [new_data[col['name']] for col in table_columns]
    cursor.execute(f"UPDATE movies SET {set_str} WHERE title=?", [*values, title])
    conn.commit()

def delete_movie(title):
    cursor.execute("DELETE FROM movies WHERE title = ?", (title,))
    conn.commit()

def search_movie(title):
    cursor.execute(f"SELECT * FROM movies WHERE title = ?", (title,))
    results = cursor.fetchall()
    for row in results:
        print(row)
    return results

# For manual testing
def test_database():
    while True:
        print("Select an operation:")
        print("1. Search movie")
        print("2. Add movie")
        print("3. Edit movie")
        print("4. Delete movie")
        print("0. Exit")

        choice = input("Enter a number: ")

        if choice == "1":
            title = input("Enter movie title: ")
            search_movie(title)

        elif choice == "2":
            data = {}
            for col in table_columns:
                value = input(f"Enter {col['name']}: ")
                data[col['name']] = value
            add_movie(data)

        elif choice == "3":
            title = input("Enter title to edit: ")
            data = {}
            for col in table_columns:
                value = input(f"Enter new {col['name']}: ")
                if value != "":
                    data[col['name']] = value
            edit_movie(title, data)

        elif choice == "4":
            title = input("Enter title to delete: ")
            delete_movie(title)

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please enter a number between 0 and 4.")

create_table()
# test_database()
conn.close()