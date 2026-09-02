import sqlite3

# This creates a new database file called bookstore.db
# If the file already exists, it connects to it
connection = sqlite3.connect("bookstore.db")

# A cursor is what you use to execute SQL commands
cursor = connection.cursor()

print("Connected to database!")

# Create a customer's table
cursor.execute(""" CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
    )
"""
)
connection.commit()
print("Customers table created")

# CREATE TABLE IF NOT EXISTS: Make a new table, but don't crash if it already exists
# id INTEGER PRIMARY KEY AUTOINCREMENT: An integer column that automatically assigns the next number (1, 2, 3...) to each new row
# name TEXT NOT NULL: A text column that cannot be left empty 
# email TEXT UNIQUE NOT NULL: A text column that must be unique across all rows and cannot be empty 
# rules (NOT NULL, UNIQUE) are called constraints

cursor.execute("""INSERT OR IGNORE INTO customers(name, email)
Values ('Maria Santos', 'maria@email.com')
""")

cursor.execute("""
    INSERT OR IGNORE INTO customers (name, email) 
    VALUES ('James Chen', 'james@email.com')
""")

# Insert multiple customers at once
more_customers = [
    ("Aisha Johnson", "aisha@email.com"),
    ("David Kim", "david@email.com"),
]
cursor.executemany("""
    INSERT OR IGNORE INTO customers (name, email) VALUES (?, ?) 
""", more_customers)

#Notice the ? placeholders in executemany. These are parameterized queries; they prevent a security vulnerability called SQL injection. Never build SQL strings with f-strings or string concatenation. Always use ? placeholders!

connection.commit()
print("Customers inserted!")

cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()

print("All customers:")
for row in rows:
    print(f"  ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")

connection.close()
print("Connection closed.")