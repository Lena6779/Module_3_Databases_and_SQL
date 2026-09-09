import sqlite3
import pandas as pd

# Step 1: SETUP SQL DB and Pandas DF with the same data below

# Set up the SQL Database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE sales(
    id INTEGER PRIMARY KEY,
    product TEXT NOT NULL,
    category TEXT NOT NULL, 
    unit_price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    quarter TEXT NOT NULL
)
""")

sales_data = [
    ("Widget A", "Electronics", 29.99, 150, "2025-Q1"),
    ("Widget B", "Electronics", 49.99, 89, "2025-Q1"),
    ("Gadget X", "Accessories", 15.99, 300, "2025-Q1"),
    ("Widget A", "Electronics", 29.99, 200, "2025-Q2"),
    ("Gadget Y", "Accessories", 22.99, 175, "2025-Q2"),
    ("Widget C", "Electronics", 79.99, 50, "2025-Q2"),
    ("Gadget X", "Accessories", 15.99, 280, "2025-Q2"),
    ("Widget B", "Electronics", 49.99, 120, "2025-Q3"),
]
# columns: product, category, unit_price, quantity, quarter

cursor.executemany(
    "INSERT INTO sales (product, category, unit_price, quantity, quarter) VALUES (?, ?, ?, ?, ?)",
    sales_data
)
conn.commit()

# TEST
cursor.execute("SELECT * FROM sales")
print(cursor.fetchall())

# --- Set up the same data as a pandas DataFrame ---
df = pd.DataFrame(sales_data, columns=["product", "category", "unit_price", "quantity", "quarter"])

print("Data loaded in both SQL and pandas!\n")

# Question 1: What is the total revenue (price × quantity) per product?
print("Question 1: What is the total revenue (price x quantity) per product?")

# --- SQL ---

#Needed to be round to 2 decimal places
cursor.execute("""
    SELECT product, ROUND(SUM(unit_price * quantity), 2) AS total_revenue   
    FROM sales
    GROUP BY product
""")
print(cursor.fetchall())

# --- Pandas ---

df["revenue"] = df["unit_price"] * df["quantity"]
revenue_by_product = df.groupby("product")["revenue"].sum()
print(revenue_by_product)

# Question 2: Which quarter had the highest total quantity sold?
print("Which quarter had the highest total quantity sold?")

# ---SQL---
cursor.execute("""
    SELECT quarter, SUM(quantity) AS total_quantity
    FROM sales
    GROUP BY quarter
    ORDER BY total_quantity DESC
    LIMIT 1
""")
print(cursor.fetchone())

# --- Pandas ---
quantity_by_quarter = df.groupby("quarter")["quantity"].sum()
print(quantity_by_quarter)

top_quarter = quantity_by_quarter.idxmax()
top_value = quantity_by_quarter.max()
print(f"{top_quarter}: {top_value}")

# Question 3: What is the average unit price per category?

# ---SQL---
cursor.execute("""
    SELECT category, ROUND(AVG(unit_price), 2) AS avg_unit_price
    FROM sales
    GROUP BY category
""")
print(cursor.fetchall())

# --- Pandas ---
avg_price_by_category = df.groupby("category")["unit_price"].mean().round(2)
print(avg_price_by_category)

# Question 4: Which products had total quantity over 200 across all quarters?

# ---SQL---
cursor.execute("""
    SELECT product, SUM(quantity) AS total_quantity
    FROM sales
    GROUP BY product
    HAVING total_quantity > 200
""")
print(cursor.fetchall())

# --- Pandas ---
quantity_by_product = df.groupby("product")["quantity"].sum()
result = quantity_by_product[quantity_by_product > 200]
print(result)

# BONUS: Use pd.read_sql() to run one of your SQL queries and get the result as a DataFrame

print("\n=== pandas.read_sql(): Best of Both Worlds ===")

query = """
    SELECT category, ROUND(AVG(unit_price), 2) AS avg_unit_price
    FROM sales
    GROUP BY category
"""

# ---SQL---
cursor.execute(query)
print(cursor.fetchall())

# read_sql runs the SQL query and returns a DataFrame
result_df = pd.read_sql(query, conn)
print(result_df.to_string(index=False))