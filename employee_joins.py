import sqlite3

connection = sqlite3.connect(":memory:")  # In-memory DB — disappears when script ends. (:memory:) creates a temporary database that lives in RAM. Perfect for practice and no file cleanup is needed.
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

# Departments table
cursor.execute("""
    CREATE TABLE departments ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL
    )
""")

# Employees table — connects students to courses
cursor.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department_id INTEGER NOT NULL,
        salary REAL,
        FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    """)

# Projects table - 
cursor.execute ("""
    CREATE TABLE projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        employee_id INTEGER NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
        )
    """)

print("Tables created!")

# SAMPLE DATA FOR INSERTION

# Add some departments
departments = [
    ("Human Resources", "New York"),    
    ("IT", "San Francisco"),
    ("Marketing", "Atlanta"),
    ("Investigation", "Washington D.C."),
    ("Sales", "Chicago"),
    ("Finance", "Boston")
]

cursor.executemany("INSERT INTO departments (name, location) VALUES (?, ?)", departments)
connection.commit()
connection.commit()

# Add some employees
employees = [
    ("Lauren", 2, 75000.00),  # IT
    ("Bo", 3, 95000.00),    # Marketing
    ("Dyson", 4, 105000.00), # Investigation
    ("Tamsin", 4, 65000.00),   # Investigation
    ("Mark", 4, 85000.00),    # Investigation
    ("Vex", 5, 90000.00),    # Sales
    ("Trick", 1, 80000.00)    # Human Resources
]
cursor.executemany("INSERT INTO employees (name, department_id, salary) VALUES (?, ?, ?)", employees)
connection.commit()

# Add some projects
projects = [
    ("Project A", 1),  # Lauren
    ("Project B", 2),  # Bo
    ("Project C", 3),  # Dyson
    ("Project D", 4),  # Tamsin
    ("Project E", 5),  # Mark
]
cursor.executemany("INSERT INTO projects (title, employee_id) VALUES (?, ?)", projects)
connection.commit() 

# QUERIES BELOW!

# Query 1 
"""List all employees with their department name(INNER JOIN)"""
print("\nList of all employees with their department name:")
cursor.execute("SELECT employees.name, departments.name FROM employees INNER JOIN departments ON employees.department_id = departments.id")
for row in cursor.fetchall():
    print(f"Employee: {row[0]}, Department: {row[1]}")

# Query 2 
"""List all departments, even those with no employees(LEFT JOIN)"""
print("\nList of all departments, even those with no employees:")
cursor.execute("SELECT departments.name FROM departments LEFT JOIN employees ON departments.id = employees.department_id")
for row in cursor.fetchall():
    print(f"Department: {row[0]}")

# Query 3
"""List all employees and the projects they lead, including those without leading projects (LEFT JOIN + IS NULL)"""
print("\nList of all employees and the projects they lead, including those without leading projects:")
cursor.execute("SELECT employees.name, projects.title FROM employees LEFT JOIN projects ON employees.id = projects.employee_id")
for row in cursor.fetchall():
    project_title = row[1] if row[1] is not None else "No Project"
    print(f"Employee: {row[0]}, Project: {project_title}")

# Query 4
"""List all employees who DO NOT lead any projects (LEFT JOIN + IS NULL)"""
print("\nList of all employees who do not lead any projects:")
cursor.execute("SELECT employees.name FROM employees LEFT JOIN projects ON employees.id = projects.employee_id WHERE projects.employee_id IS NULL")
for row in cursor.fetchall():
    print(f"Employee: {row[0]}")

# Query 5
"""List all projects with the project's lead employee's name AND their department name(requires 3 tables)"""
print("\nList of all projects with the project's lead employee's name AND their department name:")
cursor.execute("SELECT projects.title, employees.name, departments.name FROM projects LEFT JOIN employees ON projects.employee_id = employees.id LEFT JOIN departments ON employees.department_id = departments.id")
for row in cursor.fetchall():
    print(f"Project: {row[0]}, Lead Employee: {row[1]}, Department: {row[2]}")