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

## Testing

Run the unit tests:

```bash
python -m unittest
```
