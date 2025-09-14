from __future__ import annotations
import sqlite3
from datetime import date
from typing import List, Optional, Tuple

from school_db import get_connection, init_db


# --- CRUD operations ---

def add_teacher(first_name: str, last_name: str, email: str | None = None) -> int:
    conn = get_connection()
    init_db(conn)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO teacher(first_name, last_name, email) VALUES (?, ?, ?)",
        (first_name, last_name, email),
    )
    conn.commit()
    return cur.lastrowid


def list_teachers() -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute("SELECT * FROM teacher ORDER BY last_name, first_name")
    return cur.fetchall()


def get_teacher(teacher_id: int) -> sqlite3.Row | None:
    conn = get_connection()
    cur = conn.execute("SELECT * FROM teacher WHERE id = ?", (teacher_id,))
    return cur.fetchone()


def update_teacher(teacher_id: int, first_name: str, last_name: str, email: str | None) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE teacher SET first_name = ?, last_name = ?, email = ? WHERE id = ?",
        (first_name, last_name, email, teacher_id),
    )
    conn.commit()


def delete_teacher(teacher_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM teacher WHERE id = ?", (teacher_id,))
    conn.commit()


def get_teacher_courses(teacher_id: int) -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute(
        "SELECT * FROM course WHERE teacher_id = ? ORDER BY name",
        (teacher_id,),
    )
    return cur.fetchall()


def get_teacher_students(teacher_id: int) -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute(
        """
        SELECT DISTINCT s.*
        FROM student s
        JOIN enrollment e ON s.id = e.student_id
        JOIN course c ON e.course_id = c.id
        WHERE c.teacher_id = ?
        ORDER BY s.last_name, s.first_name
        """,
        (teacher_id,),
    )
    return cur.fetchall()


def get_teacher_evaluations(teacher_id: int) -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute(
        """
        SELECT s.first_name || ' ' || s.last_name AS student_name,
               c.name AS course_name,
               e.grade
        FROM enrollment e
        JOIN student s ON e.student_id = s.id
        JOIN course c ON e.course_id = c.id
        WHERE c.teacher_id = ? AND e.grade IS NOT NULL
        ORDER BY c.name, student_name
        """,
        (teacher_id,),
    )
    return cur.fetchall()


def get_enrollments_for_course(course_id: int) -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute(
        """
        SELECT e.id, s.first_name || ' ' || s.last_name AS student_name,
               e.grade, e.status
        FROM enrollment e
        JOIN student s ON e.student_id = s.id
        WHERE e.course_id = ?
        ORDER BY student_name
        """,
        (course_id,),
    )
    return cur.fetchall()


def add_course(name: str, credits: int, teacher_id: int | None) -> int:
    conn = get_connection()
    init_db(conn)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO course(name, credits, teacher_id) VALUES (?, ?, ?)",
        (name, credits, teacher_id),
    )
    conn.commit()
    return cur.lastrowid


def list_courses() -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute(
        "SELECT c.*, t.first_name || ' ' || t.last_name AS teacher_name "
        "FROM course c LEFT JOIN teacher t ON c.teacher_id = t.id"
        " ORDER BY c.name"
    )
    return cur.fetchall()


def add_program(name: str, description: str | None = None) -> int:
    conn = get_connection()
    init_db(conn)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO program(name, description) VALUES (?, ?)",
        (name, description),
    )
    conn.commit()
    return cur.lastrowid


def list_programs() -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute("SELECT * FROM program ORDER BY name")
    return cur.fetchall()


def add_student(first_name: str, last_name: str, student_number: str, email: str | None = None) -> int:
    conn = get_connection()
    init_db(conn)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO student(first_name, last_name, student_number, email) VALUES (?, ?, ?, ?)",
        (first_name, last_name, student_number, email),
    )
    conn.commit()
    return cur.lastrowid


def list_students() -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute("SELECT * FROM student ORDER BY last_name, first_name")
    return cur.fetchall()


def get_student(student_id: int) -> sqlite3.Row | None:
    conn = get_connection()
    cur = conn.execute("SELECT * FROM student WHERE id = ?", (student_id,))
    return cur.fetchone()


def update_student(
    student_id: int,
    first_name: str,
    last_name: str,
    student_number: str,
    email: str | None,
) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE student SET first_name = ?, last_name = ?, student_number = ?, email = ? WHERE id = ?",
        (first_name, last_name, student_number, email, student_id),
    )
    conn.commit()


def delete_student(student_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE id = ?", (student_id,))
    conn.commit()


def get_student_enrollments(student_id: int) -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute(
        """
        SELECT e.*, c.name AS course_name
        FROM enrollment e
        JOIN course c ON e.course_id = c.id
        WHERE e.student_id = ?
        ORDER BY c.name
        """,
        (student_id,),
    )
    return cur.fetchall()


def get_student_grades(student_id: int) -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute(
        """
        SELECT e.*, c.name AS course_name
        FROM enrollment e
        JOIN course c ON e.course_id = c.id
        WHERE e.student_id = ? AND e.grade IS NOT NULL
        ORDER BY c.name
        """,
        (student_id,),
    )
    return cur.fetchall()


def assign_course_to_program(program_id: int, course_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO program_course(program_id, course_id) VALUES (?, ?)",
        (program_id, course_id),
    )
    conn.commit()


def enroll_student_in_program(student_id: int, program_id: int, start_date: Optional[date] = None) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO student_program(student_id, program_id, start_date) VALUES (?, ?, ?)",
        (student_id, program_id, start_date.isoformat() if start_date else None),
    )
    conn.commit()


def enroll_student_in_course(student_id: int, course_id: int, semester: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO enrollment(student_id, course_id, semester, status) VALUES (?, ?, ?, ?)",
        (student_id, course_id, semester, 'enrolled'),
    )
    conn.commit()
    return cur.lastrowid


def record_grade(enrollment_id: int, grade: str, status: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE enrollment SET grade = ?, status = ? WHERE id = ?",
        (grade, status, enrollment_id),
    )
    conn.commit()


# --- Query functions ---

def get_student_progress(student_id: int, program_id: int) -> Tuple[int, int, int]:
    """Return (passed, remaining, failed_attempts)."""
    conn = get_connection()
    cur = conn.cursor()

    # total courses in program
    cur.execute(
        "SELECT COUNT(*) FROM program_course WHERE program_id = ?",
        (program_id,),
    )
    total = cur.fetchone()[0]

    # passed courses
    cur.execute(
        """
        SELECT COUNT(*) FROM enrollment e
        JOIN program_course pc ON e.course_id = pc.course_id AND pc.program_id = ?
        WHERE e.student_id = ? AND e.status = 'completed' AND e.grade != 'F'
        """,
        (program_id, student_id),
    )
    passed = cur.fetchone()[0]

    # failed attempts
    cur.execute(
        """
        SELECT COUNT(*) FROM enrollment e
        JOIN program_course pc ON e.course_id = pc.course_id AND pc.program_id = ?
        WHERE e.student_id = ? AND e.status = 'failed'
        """,
        (program_id, student_id),
    )
    failed = cur.fetchone()[0]

    remaining = max(total - passed, 0)
    return passed, remaining, failed


def get_most_popular_courses(limit: int = 5) -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute(
        """
        SELECT c.id, c.name, COUNT(e.id) AS cnt
        FROM course c LEFT JOIN enrollment e ON c.id = e.course_id
        GROUP BY c.id
        ORDER BY cnt DESC, c.name
        LIMIT ?
        """,
        (limit,),
    )
    return cur.fetchall()


def get_most_popular_teachers(limit: int = 5) -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute(
        """
        SELECT t.id, t.first_name || ' ' || t.last_name AS name, COUNT(e.id) AS cnt
        FROM teacher t
        LEFT JOIN course c ON t.id = c.teacher_id
        LEFT JOIN enrollment e ON c.id = e.course_id
        GROUP BY t.id
        ORDER BY cnt DESC, name
        LIMIT ?
        """,
        (limit,),
    )
    return cur.fetchall()


def get_best_students(limit: int = 5) -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute(
        """
        SELECT s.id, s.first_name || ' ' || s.last_name AS name,
               AVG(CASE e.grade
                       WHEN 'A' THEN 5 WHEN 'B' THEN 4 WHEN 'C' THEN 3
                       WHEN 'D' THEN 2 WHEN 'E' THEN 1 ELSE 0 END) AS avg_grade
        FROM student s
        JOIN enrollment e ON s.id = e.student_id AND e.status = 'completed'
        GROUP BY s.id
        HAVING COUNT(e.id) > 0
        ORDER BY avg_grade DESC
        LIMIT ?
        """,
        (limit,),
    )
    return cur.fetchall()


def get_at_risk_students(limit: int = 5) -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.execute(
        """
        SELECT s.id, s.first_name || ' ' || s.last_name AS name,
               SUM(CASE WHEN e.status = 'failed' THEN 1 ELSE 0 END) AS failed,
               SUM(CASE WHEN e.status = 'completed' AND e.grade != 'F' THEN 1 ELSE 0 END) AS passed
        FROM student s
        LEFT JOIN enrollment e ON s.id = e.student_id
        GROUP BY s.id
        HAVING failed > passed
        ORDER BY failed DESC
        LIMIT ?
        """,
        (limit,),
    )
    return cur.fetchall()
