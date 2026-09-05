# Step 1: Create the tables
import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

# Students table
cursor.execute("""
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
""")

# Courses table
cursor.execute("""
    CREATE TABLE courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        instructor TEXT NOT NULL,
        credits INTEGER NOT NULL
    )
""")

# Enrollments table — connects students to courses
cursor.execute("""
    CREATE TABLE enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        grade TEXT,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )
""")

print("Tables created!")

# Step 3: INNER JOIN — Students with their courses
print("\n=== Student Enrollments (INNER JOIN) ===")
cursor.execute("""
    SELECT s.name, c.title, e.grade
    FROM enrollments e
    INNER JOIN students s ON e.student_id = s.id
    INNER JOIN courses c ON e.course_id = c.id
    ORDER BY s.name, c.title
""")

for row in cursor.fetchall():
    grade = row[2] if row[2] else "Not graded"
    print(f"  {row[0]} — {row[1]}: {grade}")

# Step 4: LEFT JOIN — All students, even those not enrolled
print("\n=== All Students with Enrollment Status (LEFT JOIN) ===")
cursor.execute("""
    SELECT s.name, c.title
    FROM students s
    LEFT JOIN enrollments e ON s.id = e.student_id
    LEFT JOIN courses c ON e.course_id = c.id
    ORDER BY s.name
""")

for row in cursor.fetchall():
    course = row[1] if row[1] else "Not enrolled in any course"
    print(f"  {row[0]} — {course}")

# Step 5: Finding students NOT enrolled in anything
print("\n=== Students Not Enrolled in Any Course ===")
cursor.execute("""
    SELECT s.name, s.email
    FROM students s
    LEFT JOIN enrollments e ON s.id = e.student_id
    WHERE e.id IS NULL
""")

for row in cursor.fetchall():
    print(f"  {row[0]} ({row[1]})")

# Step 6:  A practical question — "How many students are in each course?"
print("\n=== Students Per Course ===")
cursor.execute("""
    SELECT c.title, COUNT(e.student_id) as student_count
    FROM courses c
    LEFT JOIN enrollments e ON c.id = e.course_id
    GROUP BY c.id, c.title
    ORDER BY student_count DESC
""")

for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} student(s)")

connection.close()