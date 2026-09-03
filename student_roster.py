"""A small SQLite-backed student roster with basic CRUD operations."""
 
import sqlite3
 
DB_PATH = "school.db"
 
 
def get_connection():
    """Create a connection to the school database with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
 
 
# Single connection used by every function below, so the CRUD functions can match the required signatures (no `connection` parameter).
connection = get_connection()
 
 
def create_table():
    """Create the students table if it doesn't already exist."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            gpa REAL
        )
        """
    )
    connection.commit()
 
 
# ---------------------------------------------------------------------------
# CRUD operations
# ---------------------------------------------------------------------------
 
def add_student(name, grade, gpa):
    """Insert a new student and return their new id."""
    cursor = connection.execute(
        "INSERT INTO students (name, grade, gpa) VALUES (?, ?, ?)",
        (name, grade, gpa),
    )
    connection.commit()
    return cursor.lastrowid
 
 
def get_all_students():
    """Return a list of all students as (id, name, grade, gpa) tuples."""
    cursor = connection.execute("SELECT id, name, grade, gpa FROM students")
    return cursor.fetchall()
 
 
def get_student_by_id(student_id):
    """Return a single student by id, or None if not found."""
    cursor = connection.execute(
        "SELECT id, name, grade, gpa FROM students WHERE id = ?",
        (student_id,),
    )
    return cursor.fetchone()
 
 
def update_student_gpa(student_id, new_gpa):
    """Update a student's GPA. Returns True if a row was updated."""
    cursor = connection.execute(
        "UPDATE students SET gpa = ? WHERE id = ?",
        (new_gpa, student_id),
    )
    connection.commit()
    return cursor.rowcount > 0  # Return True if a row was updated. Any count above 0 means a row was updated. Exactly 0 means no row was updated. Example: If 1 row is updated, cursor.rowcount will be 1, so the function returns True.
 
 
def delete_student(student_id):
    """Remove a student by id. Returns True if a row was deleted."""
    cursor = connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,),
    )
    connection.commit()
    return cursor.rowcount > 0  # Return True if a row was deleted. Any count above 0 means a row was deleted. Exactly 0 means no row was deleted. Example: If 1 row is deleted, cursor.rowcount will be 1, so the function returns True.
 
 
# ---------------------------------------------------------------------------
# Demo With Student Data 
# ---------------------------------------------------------------------------
 
def print_students(students):
    if not students:
        print("  (no students)")
        return
    for student_id, name, grade, gpa in students:
        gpa_display = f"{gpa:.2f}" if gpa is not None else "N/A"
        print(f"  [{student_id}] {name} - Grade {grade}, GPA {gpa_display}")
 
 
def main():
    create_table()
 
    # Add at least 4 students, but only seed on a fresh/empty table so re-running the script doesn't keep piling up duplicate rows like adding Alice Johnson twice. That was a problem that I fixed here below.
    if not get_all_students():
        print("No students found - seeding initial data...")
        add_student("Alice Johnson", 10, 3.7)
        add_student("Bob Smith", 11, 3.6)
        add_student("Claire Wilson", 12, 3.9)
        add_student("David Wilson", 12, 3.8)
    else:
        print("Existing students found - skipping seed data.")
 
    # Print all students
    print("\nAll students:")
    students = get_all_students()
    print_students(students)
 
    # Update one student's GPA (the last student currently in the table, looked up by actual id rather than a hard-coded one)
    student_to_update_id, student_to_update_name = students[-1][0], students[-1][1]
    print(f"\nUpdating GPA for student {student_to_update_id} ({student_to_update_name}) to 4.0...")
    update_student_gpa(student_to_update_id, 4.0)
 
    # Delete one student (the first student currently in the table, looked up by actual id rather than a hard-coded one)
    student_to_delete_id, student_to_delete_name = students[0][0], students[0][1]
    print(f"Deleting student {student_to_delete_id} ({student_to_delete_name})...")
    delete_student(student_to_delete_id)
 
    # Print all students again to confirm changes
    print("\nAll students after updates:")
    print_students(get_all_students())
 
    connection.close()
 
 
if __name__ == "__main__":
    main()