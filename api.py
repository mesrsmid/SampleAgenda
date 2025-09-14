from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from school_db import get_connection
from school_service import (
    add_course,
    add_student,
    add_teacher,
    enroll_student_in_course,
    list_courses,
    list_students,
    list_teachers,
)

app = FastAPI(title="SampleAgenda API")


class TeacherIn(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None


class Teacher(TeacherIn):
    id: int


class CourseIn(BaseModel):
    name: str
    credits: int
    teacher_id: Optional[int] = None


class Course(BaseModel):
    id: int
    name: str
    credits: int
    teacher_id: Optional[int] = None
    teacher_name: Optional[str] = None


class StudentIn(BaseModel):
    first_name: str
    last_name: str
    student_number: str
    email: Optional[str] = None


class Student(StudentIn):
    id: int


class EnrollmentIn(BaseModel):
    student_id: int
    course_id: int
    semester: str


class Enrollment(BaseModel):
    id: int
    student_id: int
    course_id: int
    semester: str
    status: str
    grade: Optional[str] = None


def _get_row(table: str, pk: int):
    conn = get_connection()
    cur = conn.execute(f"SELECT * FROM {table} WHERE id=?", (pk,))
    return cur.fetchone()


@app.post("/teachers", response_model=Teacher, status_code=201)
def create_teacher(data: TeacherIn) -> Teacher:
    tid = add_teacher(data.first_name, data.last_name, data.email)
    return Teacher(id=tid, **data.dict())


@app.get("/teachers", response_model=List[Teacher])
def read_teachers() -> List[Teacher]:
    return [Teacher(**dict(row)) for row in list_teachers()]


@app.post("/courses", response_model=Course, status_code=201)
def create_course(data: CourseIn) -> Course:
    if data.teacher_id is not None and not _get_row("teacher", data.teacher_id):
        raise HTTPException(status_code=404, detail="Teacher not found")
    cid = add_course(data.name, data.credits, data.teacher_id)
    conn = get_connection()
    row = conn.execute(
        "SELECT c.*, t.first_name || ' ' || t.last_name AS teacher_name "
        "FROM course c LEFT JOIN teacher t ON c.teacher_id = t.id WHERE c.id=?",
        (cid,),
    ).fetchone()
    return Course(**dict(row))


@app.get("/courses", response_model=List[Course])
def read_courses() -> List[Course]:
    return [Course(**dict(row)) for row in list_courses()]


@app.post("/students", response_model=Student, status_code=201)
def create_student(data: StudentIn) -> Student:
    sid = add_student(
        data.first_name, data.last_name, data.student_number, data.email
    )
    return Student(id=sid, **data.dict())


@app.get("/students", response_model=List[Student])
def read_students() -> List[Student]:
    return [Student(**dict(row)) for row in list_students()]


@app.post("/enrollments", response_model=Enrollment, status_code=201)
def enroll(data: EnrollmentIn) -> Enrollment:
    if not _get_row("student", data.student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    if not _get_row("course", data.course_id):
        raise HTTPException(status_code=404, detail="Course not found")
    eid = enroll_student_in_course(data.student_id, data.course_id, data.semester)
    conn = get_connection()
    row = conn.execute("SELECT * FROM enrollment WHERE id=?", (eid,)).fetchone()
    return Enrollment(**dict(row))
