# SampleAgenda

This project provides a minimal command line information system for schools.
It stores teachers, courses, study programs, students and enrollments in a
SQLite database and offers basic analytics such as student progress or popular
courses.

## Usage

Initialize the database:

```bash
python main.py init-db
```

Add a teacher:

```bash
python main.py add-teacher John Doe john@example.com
```

List teachers:

```bash
python main.py list-teachers
```

See `python main.py -h` for all available commands.

## API

Run the web service:

```bash
uvicorn api:app --reload
```

Add a teacher:

```bash
curl -X POST http://localhost:8000/teachers   -H "Content-Type: application/json"   -d '{"first_name":"John","last_name":"Doe","email":"john@example.com"}'
```

List teachers:

```bash
curl http://localhost:8000/teachers
```

Enroll a student in a course:

```bash
curl -X POST http://localhost:8000/enrollments   -H "Content-Type: application/json"   -d '{"student_id":1,"course_id":1,"semester":"2024S"}'
```


## Testing

Run the unit tests:

```bash
python -m unittest
```
