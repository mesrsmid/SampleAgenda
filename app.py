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
