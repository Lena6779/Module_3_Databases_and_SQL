import sqlite3

connection = sqlite3.connect(":memory:")  # In-memory DB — disappears when script ends. (:memory:) creates a temporary database that lives in RAM. Perfect for practice and no file cleanup is needed.
cursor = connection.cursor()

# Create a products table
cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        rating REAL,
        in_stock INTEGER DEFAULT 1
    )
""")

# Insert sample data — a small electronics store
products = [
    ("Wireless Mouse", "Accessories", 29.99, 4.5, 1),
    ("Mechanical Keyboard", "Accessories", 89.99, 4.8, 1),
    ("USB-C Hub", "Accessories", 34.99, 4.2, 0),
    ("27-inch Monitor", "Displays", 299.99, 4.6, 1),
    ("24-inch Monitor", "Displays", 179.99, 4.3, 1),
    ("Webcam HD", "Accessories", 49.99, 3.9, 1),
    ("Noise-Canceling Headphones", "Audio", 199.99, 4.7, 1),
    ("Bluetooth Speaker", "Audio", 59.99, 4.1, 0),
    ("Laptop Stand", "Accessories", 39.99, 4.4, 1),
    ("External SSD 1TB", "Storage", 89.99, 4.6, 1),
    ("External SSD 2TB", "Storage", 149.99, 4.5, 1),
    ("Flash Drive 64GB", "Storage", 12.99, 4.0, 1),
]

cursor.executemany("""
    INSERT INTO products (name, category, price, rating, in_stock) 
    VALUES (?, ?, ?, ?, ?)
""", products)
connection.commit()

# Question 1: Which products are out of stock? Show name and category.
print("\n=== Out of Stock Products ===")
cursor.execute("SELECT name, category FROM products WHERE in_stock = 0")
for row in cursor.fetchall():
    print(f" {row[0]}: {row[1]}")

# Question 2: Which products have the a rating of 4.5 or higher AND costs less than $100? Show name, rating, and price. 
print("\n=== Products with Rating 4.5 or Higher AND costs less than $100 ===")
cursor.execute("SELECT name, rating, price FROM products WHERE rating >= 4.5 AND price < 100.00")
for row in cursor.fetchall():
    print(f" {row[0]}: Rating {row[1]}, Price ${row[2]:.2f}")


# Question 3: What are the 3 most expensive products in the "Accessories" category? (Show name and price, sorted by price descending) 
print("\n=== 3 Most Expensive Accessories ===")
cursor.execute("SELECT name, price FROM products WHERE category = 'Accessories' ORDER BY price DESC LIMIT 3")
for row in cursor.fetchall():
    print(f" {row[0]}: ${row[1]:.2f}")

# Question 4: Which products have "Monitor" in their name? (Show all columns)
print("\n=== Products with 'Monitor' in Name ===")
cursor.execute("SELECT * FROM products WHERE name LIKE '%Monitor%'")
for row in cursor.fetchall():
    print(f" ID: {row[0]}, Name: {row[1]}, Category: {row[2]}, Price: ${row[3]:.2f}, Rating: {row[4]}, In Stock: {'Yes' if row[5] == 1 else 'Not in stock'}")

# Question 5: Which products are NOT in the "Accessories" category and are in stock? (Show name, category, price, sorted by category then price)
print("\n=== Products NOT in 'Accessories' Category AND are in Stock ===")
cursor.execute("SELECT name, category, price FROM products WHERE category != 'Accessories' AND in_stock = 1 ORDER BY category, price")
for row in cursor.fetchall():
    print(f" {row[0]}: {row[1]}, ${row[2]:.2f}")