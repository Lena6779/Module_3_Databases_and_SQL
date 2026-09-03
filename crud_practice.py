import sqlite3

connection = sqlite3.connect("bookstore.db")
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        price REAL NOT NULL,
        in_stock INTEGER DEFAULT 1
    )
""")

books = [
    ("Dune", "Frank Herbert", 15.99, 1),
    ("Neuromancer", "William Gibson", 12.99, 1),
    ("Snow Crash", "Neal Stephenson", 14.99, 1),
    ("The Left Hand of Darkness", "Ursula K. Le Guin", 13.99, 0),
    ("Kindred", "Octavia Butler", 11.99, 1),
]
cursor.executemany("""
    INSERT OR IGNORE INTO books (title, author, price, in_stock)
    VALUES (?, ?, ?, ?)
""", books)
connection.commit()

# Step 2: READ and SELECT
print("=== All Books ===")
cursor.execute("SELECT * FROM books")
for row in cursor.fetchall():
    status = "In Stock" if row[4] else "Out of Stock"
    print(f"  [{row[0]}] {row[1]} by {row[2]} — ${row[3]:.2f} ({status})")

# Step 3: CREATE
cursor.execute("""
    INSERT INTO books (title, author, price, in_stock) VALUES (?, ?, ?, ?)
""", ("Foundation", "Isaac Asimov", 13.49, 1))
connection.commit()

# Step 4: UPDATE
cursor.execute("UPDATE books SET price = 17.99 WHERE id = 1")
connection.commit()

# Step 5: DELETE
cursor.execute("DELETE FROM books WHERE id = 3")
connection.commit()

cursor.execute("SELECT id, title FROM books")
for row in cursor.fetchall():
    print(f"  [{row[0]}] {row[1]}")

connection.close()

# Step 6: WRAPPING CRUD in functions

def add_book(title, author, price, in_stock=1):
    cursor.execute(
        "INSERT INTO books (title, author, price, in_stock) VALUES (?, ?, ?, ?)",
        (title, author, price, in_stock)
    )
    connection.commit()

def get_all_books():
    cursor.execute("SELECT * FROM books")
    return cursor.fetchall()

def update_book_price(book_id, new_price):
    cursor.execute("UPDATE books SET price = ? WHERE id = ?", (new_price, book_id))
    connection.commit()

def delete_book(book_id):
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    connection.commit()

# The same Create, Update, and Delete operations from steps 3-5 are now single function calls! As seen below:
add_book("Foundation", "Isaac Asimov", 13.49)
update_book_price(1, 17.99)
delete_book(3)

for row in get_all_books():
    print(row)


# This is the same pattern you'll use in the practice exercise: one function per operation, called from a main block.

# Key takeaways:

# fetchall() returns a list of tuples (all matching rows)
# fetchone() returns a single tuple (or None)
# Always commit() after INSERT, UPDATE, or DELETE
# Always use ? placeholders for values
# Always include WHERE on UPDATE and DELETE
# Wrap each operation in its own function so it can be reused and tested