import sqlite3

connection = sqlite3.connect(":memory:") 
cursor = connection.cursor()

# Create tables
cursor.execute("""
    CREATE TABLE members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        join_date TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT NOT NULL,
        year_published INTEGER NOT NULL
    )
    """)

cursor.execute("""
    CREATE TABLE checkouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        checkout_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY (member_id) REFERENCES members (id),
        FOREIGN KEY (book_id) REFERENCES books (id)
    )
""")

# Insert sample data into members table
cursor.executemany("""
    INSERT INTO members (name, join_date) VALUES (?, ?)
""", [
    ("Alice Johnson", "2023-01-15"),
    ("Bob Smith", "2023-02-20"),
    ("Charlie Brown", "2023-03-10"),
    ("Diana Prince", "2023-04-05"),
    ("Barbara Gordon", "2023-05-12"),
    ("Bruce Wayne", "2023-06-18"),
    ("Clark Kent", "2023-07-22"),
    ("Lois Lane", "2023-08-30"),
    ("Ethan Hunt", "2023-09-14"),
    ("Fiona Gallagher", "2023-10-01"),
])

# Insert sample data into books table
cursor.executemany("""
    INSERT INTO books (title, genre, year_published) VALUES (?, ?, ?)
""", [
    ("The Great Gatsby", "Fiction", 1925),
    ("To Kill a Mockingbird", "Fiction", 1960),
    ("1984", "Dystopian", 1949),
    ("Pride and Prejudice", "Romance", 1813),
    ("The Catcher in the Rye", "Fiction", 1951),
    ("The Hobbit", "Fantasy", 1937),
    ("Moby Dick", "Adventure", 1851),
    ("War and Peace", "Historical", 1869),
    ("The Odyssey", "Epic", -800),
    ("Crime and Punishment", "Psychological Fiction", 1866),
    ("Harry Potter and the Sorcerer's Stone", "Fantasy", 1997),
    ("The Lord of the Rings", "Fantasy", 1954),
])

# Insert sample data into checkouts table
cursor.executemany("""
    INSERT INTO checkouts (member_id, book_id, checkout_date) VALUES (?, ?, ?)
""", [
    (1, 1, "2023-01-20"),
    (2, 2, "2023-02-25"),
    (3, 3, "2023-03-15"),
    (4, 4, "2023-04-10"),
    (5, 5, "2023-05-18"),
    (6, 6, "2023-06-22"),
    (7, 7, "2023-07-28"),
    (8, 8, "2023-08-31"),
    (9, 9, "2023-09-20"),
    (10, 10, "2023-10-05"),
])

# 1. How many books are in each genre? (GROUP BY)
cursor.execute("""
    SELECT genre, COUNT(*) as book_count
    FROM books
    GROUP BY genre
""")    
print("Books in each genre:")
print(cursor.fetchall())

# 2. Which member has checked out the most books?(GROUP BY, ORDER BY, LIMIT)
cursor.execute("""
    SELECT members.name, COUNT(checkouts.id) as checkout_count
    FROM members
    JOIN checkouts ON members.id = checkouts.member_id
    GROUP BY members.id
    ORDER BY checkout_count DESC
    LIMIT 1
""")
print("\nMember with the most checkouts:")
print(cursor.fetchone())

# 3. Which is the average number of books checked out per member? (SUBQUERY OR NESTED AGGREGATION)
cursor.execute("""
    SELECT AVG(checkout_count) as avg_checkouts_per_member
    FROM (
        SELECT COUNT(checkouts.id) as checkout_count
        FROM members
        LEFT JOIN checkouts ON members.id = checkouts.member_id
        GROUP BY members.id
    )
""")
print("\nAverage checkouts per member:")
print(cursor.fetchone())

# 4. Which books have never been checked out? (LEFT JOIN, IS NULL)
cursor.execute("""
    SELECT books.title
    FROM books
    LEFT JOIN checkouts ON books.id = checkouts.book_id
    WHERE checkouts.book_id IS NULL
""")
print("\nBooks that have never been checked out:")
print(cursor.fetchall())

# 5. Summary of checkouts per month (GROUP BY, strftime)                 
# I wanted to add an extra query for fun to show how many checkout were made each month. I used the strftime function to extract the year and month from the checkout_date column and grouped the results by month. This query is helpful for how busy the library is each month and can help with planning for future events or promotions!
cursor.execute("""
    SELECT strftime('%Y-%m', checkout_date) as month, COUNT(*) as checkout_count
    FROM checkouts
    GROUP BY month
""")
print("\nCheckouts per month:")
print(cursor.fetchall())

connection.close()