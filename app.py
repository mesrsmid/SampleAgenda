from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import school_service as svc

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse(url="/courses")


@app.get("/teachers")
async def get_teachers(request: Request):
    teachers = svc.list_teachers()
    return templates.TemplateResponse("teachers.html", {"request": request, "teachers": teachers})


@app.post("/teachers/add")
async def add_teacher(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str | None = Form(None),
):
    svc.add_teacher(first_name, last_name, email)
    return RedirectResponse("/teachers", status_code=303)


@app.get("/teachers/{teacher_id}")
async def teacher_detail(request: Request, teacher_id: int):
    teacher = svc.get_teacher(teacher_id)
    courses = svc.get_teacher_courses(teacher_id)
    students = svc.get_teacher_students(teacher_id)
    evaluations = svc.get_teacher_evaluations(teacher_id)
    context = {
        "request": request,
        "teacher": teacher,
        "courses": courses,
        "students": students,
        "evaluations": evaluations,
    }
    return templates.TemplateResponse("teacher_detail.html", context)


@app.get("/teachers/{teacher_id}/edit")
async def edit_teacher_form(request: Request, teacher_id: int):
    teacher = svc.get_teacher(teacher_id)
    return templates.TemplateResponse("teacher_edit.html", {"request": request, "teacher": teacher})


@app.post("/teachers/{teacher_id}/edit")
async def edit_teacher(
    teacher_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str | None = Form(None),
):
    svc.update_teacher(teacher_id, first_name, last_name, email)
    return RedirectResponse(f"/teachers/{teacher_id}", status_code=303)


@app.post("/teachers/{teacher_id}/delete")
async def delete_teacher(teacher_id: int):
    svc.delete_teacher(teacher_id)
    return RedirectResponse("/teachers", status_code=303)


@app.get("/teachers/{teacher_id}/courses/{course_id}/grades")
async def course_grades(request: Request, teacher_id: int, course_id: int):
    enrollments = svc.get_enrollments_for_course(course_id)
    course = next((c for c in svc.get_teacher_courses(teacher_id) if c["id"] == course_id), None)
    context = {
        "request": request,
        "enrollments": enrollments,
        "course": course,
        "teacher_id": teacher_id,
    }
    return templates.TemplateResponse("course_grades.html", context)


@app.post("/teachers/{teacher_id}/courses/{course_id}/grades")
async def post_course_grade(
    teacher_id: int,
    course_id: int,
    enrollment_id: int = Form(...),
    grade: str = Form(...),
):
    svc.record_grade(enrollment_id, grade, "completed")
    return RedirectResponse(
        f"/teachers/{teacher_id}/courses/{course_id}/grades", status_code=303
    )


@app.get("/courses")
async def get_courses(request: Request):
    courses = svc.list_courses()
    return templates.TemplateResponse("courses.html", {"request": request, "courses": courses})


@app.post("/courses/add")
async def post_course(name: str = Form(...), credits: int = Form(...), teacher_id: int | None = Form(None)):
    svc.add_course(name, credits, teacher_id)
    return RedirectResponse("/courses", status_code=303)


@app.post("/enroll")
async def enroll(student_id: int = Form(...), course_id: int = Form(...), semester: str = Form(...)):
    svc.enroll_student_in_course(student_id, course_id, semester)
    return RedirectResponse("/courses", status_code=303)


@app.get("/progress")
async def progress(request: Request, student_id: int | None = None, program_id: int | None = None):
    context = {"request": request, "student_id": student_id, "program_id": program_id}
    if student_id is not None and program_id is not None:
        passed, remaining, failed = svc.get_student_progress(student_id, program_id)
        context.update({"passed": passed, "remaining": remaining, "failed": failed})
    return templates.TemplateResponse("student_progress.html", context)


@app.get("/analytics")
async def analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})


@app.get("/api/analytics/popular-courses")
async def popular_courses():
    data = svc.get_most_popular_courses()
    return [{"name": row["name"], "count": row["cnt"]} for row in data]


@app.get("/api/analytics/popular-teachers")
async def popular_teachers():
    data = svc.get_most_popular_teachers()
    return [{"name": row["name"], "count": row["cnt"]} for row in data]
