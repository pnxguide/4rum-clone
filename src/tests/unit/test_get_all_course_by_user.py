import models

def test_get_all_courses_by_user(db):
    models.con = db
    courses = models.get_all_courses_by_user('student1')
    assert len(courses) == 3
    course_names = [course['course_name'] for course in courses]
    assert 'Computer Programming 101' in course_names
    assert 'Databases In Practice' in course_names

def test_get_all_courses_by_user_no_courses(db):
    models.con = db
    courses = models.get_all_courses_by_user('student3')
    assert len(courses) == 2

def test_get_all_courses_by_user_nonexistent_user(db):
    models.con = db
    courses = models.get_all_courses_by_user('nonexistentuser')
    assert len(courses) == 0
