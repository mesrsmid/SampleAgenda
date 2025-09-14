import os
import tempfile
import unittest

import school_db
import school_service as svc


class ServiceTest(unittest.TestCase):
    def setUp(self):
        self.dbfile = tempfile.NamedTemporaryFile(delete=False)
        self.dbfile.close()
        school_db.DB_NAME = self.dbfile.name
        conn = school_db.get_connection()
        school_db.init_db(conn)

    def tearDown(self):
        os.remove(self.dbfile.name)

    def test_add_teacher_and_list(self):
        svc.add_teacher("John", "Doe", "j@example.com")
        teachers = svc.list_teachers()
        self.assertEqual(len(teachers), 1)
        self.assertEqual(teachers[0]["first_name"], "John")

    def test_student_progress(self):
        t_id = svc.add_teacher("Jane", "Smith", None)
        c_id = svc.add_course("Math", 5, t_id)
        p_id = svc.add_program("MathProgram", "desc")
        svc.assign_course_to_program(p_id, c_id)
        s_id = svc.add_student("Alice", "Brown", "S001", None)
        svc.enroll_student_in_program(s_id, p_id)
        e_id = svc.enroll_student_in_course(s_id, c_id, "2023")
        svc.record_grade(e_id, "A", "completed")
        passed, remaining, failed = svc.get_student_progress(s_id, p_id)
        self.assertEqual((passed, remaining, failed), (1, 0, 0))


if __name__ == "__main__":
    unittest.main()
