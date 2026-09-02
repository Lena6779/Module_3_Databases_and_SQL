import sqlite3

connection = sqlite3.connect("music.db")
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

print("Connected to database!")

# Creating two tables(artists and albums)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        genre TEXT NOT NULL
    )
""")

more_artists = [
    ("Justin Bieber", "Pop"),
    ("Taylor Swift", "Pop/Country"),
    ("Ed Sheeran", "Pop")
]
cursor.executemany("""
    INSERT INTO artists (name, genre) VALUES (?, ?)
""", more_artists)

connection.commit()
print("Artists added with their genere of music!")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist_id INTEGER,
        year INTEGER,
        FOREIGN KEY (artist_id) REFERENCES artists (id)
    )
""")

cursor.executemany("""
    INSERT INTO albums (title, artist_id, year) VALUES (?, ?, ?)
""", [
    ("Justice", 1, 2021),
    ("1989", 2, 2014),
    ("Play", 3, 2025)
])

connection.commit()
print("Albums added with their respective artists and release years!")

cursor.execute("SELECT * FROM artists")
rows = cursor.fetchall()

print("All artists:")
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Genre: {row[2]}")

cursor.execute("SELECT * FROM albums")
rows = cursor.fetchall()

print("All albums:")
for row in rows:
    print(f"ID: {row[0]}, Title: {row[1]}, Artist ID: {row[2]}, Year: {row[3]}")

connection.close()
print("Connection closed!")