import argparse
from datetime import datetime

from school_db import get_connection, init_db
from school_service import (
    add_course,
    add_program,
    add_student,
    add_teacher,
    assign_course_to_program,
    enroll_student_in_course,
    enroll_student_in_program,
    get_at_risk_students,
    get_best_students,
    get_most_popular_courses,
    get_most_popular_teachers,
    get_student_progress,
    list_courses,
    list_programs,
    list_students,
    list_teachers,
    record_grade,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="School information system")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init-db")

    p = sub.add_parser("add-teacher")
    p.add_argument("first")
    p.add_argument("last")
    p.add_argument("email")

    sub.add_parser("list-teachers")

    p = sub.add_parser("add-course")
    p.add_argument("name")
    p.add_argument("credits", type=int)
    p.add_argument("teacher_id", type=int, nargs="?")

    sub.add_parser("list-courses")

    p = sub.add_parser("add-program")
    p.add_argument("name")
    p.add_argument("description", nargs="?")

    sub.add_parser("list-programs")

    p = sub.add_parser("add-student")
    p.add_argument("first")
    p.add_argument("last")
    p.add_argument("student_number")
    p.add_argument("email")

    sub.add_parser("list-students")

    p = sub.add_parser("assign-course")
    p.add_argument("program_id", type=int)
    p.add_argument("course_id", type=int)

    p = sub.add_parser("enroll-program")
    p.add_argument("student_id", type=int)
    p.add_argument("program_id", type=int)
    p.add_argument("start_date", nargs="?", help="YYYY-MM-DD")

    p = sub.add_parser("enroll-course")
    p.add_argument("student_id", type=int)
    p.add_argument("course_id", type=int)
    p.add_argument("semester")

    p = sub.add_parser("record-grade")
    p.add_argument("enrollment_id", type=int)
    p.add_argument("grade")
    p.add_argument("status")

    p = sub.add_parser("student-progress")
    p.add_argument("student_id", type=int)
    p.add_argument("program_id", type=int)

    p = sub.add_parser("popular-courses")
    p.add_argument("limit", type=int, nargs="?", default=5)

    p = sub.add_parser("popular-teachers")
    p.add_argument("limit", type=int, nargs="?", default=5)

    p = sub.add_parser("best-students")
    p.add_argument("limit", type=int, nargs="?", default=5)

    p = sub.add_parser("at-risk-students")
    p.add_argument("limit", type=int, nargs="?", default=5)

    args = parser.parse_args()

    if args.command == "init-db":
        conn = get_connection()
        init_db(conn)
    elif args.command == "add-teacher":
        add_teacher(args.first, args.last, args.email)
    elif args.command == "list-teachers":
        for row in list_teachers():
            print(dict(row))
    elif args.command == "add-course":
        add_course(args.name, args.credits, args.teacher_id)
    elif args.command == "list-courses":
        for row in list_courses():
            print(dict(row))
    elif args.command == "add-program":
        add_program(args.name, args.description)
    elif args.command == "list-programs":
        for row in list_programs():
            print(dict(row))
    elif args.command == "add-student":
        add_student(args.first, args.last, args.student_number, args.email)
    elif args.command == "list-students":
        for row in list_students():
            print(dict(row))
    elif args.command == "assign-course":
        assign_course_to_program(args.program_id, args.course_id)
    elif args.command == "enroll-program":
        start = datetime.fromisoformat(args.start_date).date() if args.start_date else None
        enroll_student_in_program(args.student_id, args.program_id, start)
    elif args.command == "enroll-course":
        enroll_student_in_course(args.student_id, args.course_id, args.semester)
    elif args.command == "record-grade":
        record_grade(args.enrollment_id, args.grade, args.status)
    elif args.command == "student-progress":
        passed, remaining, failed = get_student_progress(args.student_id, args.program_id)
        print(f"passed={passed} remaining={remaining} failed={failed}")
    elif args.command == "popular-courses":
        for row in get_most_popular_courses(args.limit):
            print(dict(row))
    elif args.command == "popular-teachers":
        for row in get_most_popular_teachers(args.limit):
            print(dict(row))
    elif args.command == "best-students":
        for row in get_best_students(args.limit):
            print(dict(row))
    elif args.command == "at-risk-students":
        for row in get_at_risk_students(args.limit):
            print(dict(row))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
