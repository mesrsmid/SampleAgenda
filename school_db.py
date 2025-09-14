import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_NAME = 'school.db'


def get_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Return a SQLite connection with Row factory."""
    if db_path is None:
        db_path = DB_NAME
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Yield a connection that is closed automatically."""
    conn = get_connection(db_path)
    try:
        yield conn
    finally:
        conn.close()


def init_db(conn: sqlite3.Connection) -> None:
    """Create all tables if they do not exist."""
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS teacher (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS course (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            credits INTEGER NOT NULL,
            teacher_id INTEGER REFERENCES teacher(id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS program (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            student_number TEXT UNIQUE NOT NULL,
            email TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS program_course (
            program_id INTEGER REFERENCES program(id),
            course_id INTEGER REFERENCES course(id),
            PRIMARY KEY (program_id, course_id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS student_program (
            student_id INTEGER REFERENCES student(id),
            program_id INTEGER REFERENCES program(id),
            start_date TEXT,
            PRIMARY KEY (student_id, program_id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS enrollment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER REFERENCES student(id),
            course_id INTEGER REFERENCES course(id),
            semester TEXT,
            status TEXT,
            grade TEXT,
            UNIQUE(student_id, course_id, semester)
        )
        """
    )

    conn.commit()
