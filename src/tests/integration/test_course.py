import models

def test_create_course_add_user_to_course_valid(db):
    models.con = db
    result = models.create_course('Data Science 101')
    assert result == True
    courses = db.execute("SELECT * FROM courses WHERE name = 'Data Science 101'").fetchall()
    assert len(courses) == 1
    id = courses[0][0]
    result = models.add_user_to_course('student2', id)
    assert result == True
    user = db.execute("SELECT id FROM users WHERE username = 'student2'").fetchone()
    association = db.execute("SELECT * FROM course_users WHERE user_id = ? AND course_id = ?", [user[0], id]).fetchone()
    assert association is not None

def test_get_courses_by_user_add_user_to_course(db):
    models.con = db
    courses = models.get_all_courses_by_user('student3')
    assert len(courses) == 2

    result = models.add_user_to_course('student3', 2)
    assert result == True

    courses = models.get_all_courses_by_user('student3')
    assert len(courses) == 3

def test_create_course_add_multiple_users_to_course(db):
    models.con = db
    result = models.create_course('Machine Learning Basics')
    assert result == True
    courses = db.execute("SELECT * FROM courses WHERE name = 'Machine Learning Basics'").fetchall()
    assert len(courses) == 1
    course_id = courses[0][0]

    users_to_add = ['student1', 'student2', 'student3']
    for username in users_to_add:
        result = models.add_user_to_course(username, course_id)
        assert result == True
        user = db.execute("SELECT id FROM users WHERE username = ?", [username]).fetchone()
        association = db.execute("SELECT * FROM course_users WHERE user_id = ? AND course_id = ?", [user[0], course_id]).fetchone()
        assert association is not None

def test_create_multiple_courses_add_users_to_course(db):
    models.con = db
    course_names = ['AI Fundamentals', 'Data Structures', 'Web Development']
    for name in course_names:
        result = models.create_course(name)
        assert result == True

    for name in course_names:
        courses = db.execute("SELECT * FROM courses WHERE name = ?", [name]).fetchall()
        assert len(courses) == 1
        course_id = courses[0][0]

        result = models.add_user_to_course('student1', course_id)
        assert result == True
        user = db.execute("SELECT id FROM users WHERE username = 'student1'").fetchone()
        association = db.execute("SELECT * FROM course_users WHERE user_id = ? AND course_id = ?", [user[0], course_id]).fetchone()
        assert association is not None

def test_create_course_and_course_exsit_and_add_users_to_course(db):
    models.con = db
    names = ['Computer Programming 101', 'Cybersecurity Basics', 'Cloud Computing', 'Database Management']
    for name in names:
        if name == 'Computer Programming 101':
            result = models.create_course(name)
            assert result == False
        else:
            result = models.create_course(name)
            assert result == True

    users_to_add = ['student1', 'student2']
    for name in names:
        for username in users_to_add:
            course = db.execute("SELECT * FROM courses WHERE name = ?", [name]).fetchone()
            course_id = course[0]
            if name == 'Computer Programming 101' and (username == 'student1' or username == 'student2'):
                result = models.add_user_to_course(username, course_id)
                assert result == False
            else:
                result = models.add_user_to_course(username, course_id)
                assert result == True
                user = db.execute("SELECT id FROM users WHERE username = ?", [username]).fetchone()
                association = db.execute("SELECT * FROM course_users WHERE user_id = ? AND course_id = ?", [user[0], course_id]).fetchone()
                assert association is not None