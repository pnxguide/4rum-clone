import models

def test_add_user_to_course_valid(db):
    models.con = db
    result = models.add_user_to_course('student3', 2)
    assert result == True
    user = db.execute("SELECT id FROM users WHERE username = 'student3'").fetchone()
    course = db.execute("SELECT id FROM courses WHERE id = 3").fetchone()
    association = db.execute("SELECT * FROM course_users WHERE user_id = ? AND course_id = ?", [user[0], course[0]]).fetchone()
    assert association is not None
    cnt = db.execute("SELECT COUNT(*) FROM course_users").fetchone()[0]
    assert cnt == 8

def test_add_user_to_course_nonexistent_user(db):
    models.con = db
    result = models.add_user_to_course('nonexistentuser', 1)
    assert result == False
    associations = db.execute("SELECT * FROM course_users WHERE user_id = (SELECT id FROM users WHERE username = 'nonexistentuser')").fetchall()
    assert len(associations) == 0
    cnt = db.execute("SELECT COUNT(*) FROM course_users").fetchone()[0]
    assert cnt == 7

def test_add_user_to_course_nonexistent_course(db):
    models.con = db
    result = models.add_user_to_course('student1', 999)
    assert result == False
    user = db.execute("SELECT id FROM users WHERE username = 'student1'").fetchone()
    associations = db.execute("SELECT * FROM course_users WHERE user_id = ? AND course_id = 999", [user[0]]).fetchall()
    assert len(associations) == 0
    cnt = db.execute("SELECT COUNT(*) FROM course_users").fetchone()[0]
    assert cnt == 7

def test_add_user_to_course_already_added(db):
    models.con = db
    result = models.add_user_to_course('student1', 1)
    assert result == False
    user = db.execute("SELECT id FROM users WHERE username = 'student1'").fetchone()
    associations = db.execute("SELECT * FROM course_users WHERE user_id = ? AND course_id = 1", [user[0]]).fetchall()
    assert len(associations) == 1
    cnt = db.execute("SELECT COUNT(*) FROM course_users").fetchone()[0]
    assert cnt == 7

def test_add_user_to_course_empty_username(db):
    models.con = db
    result = models.add_user_to_course('', 1)
    assert result == False
    associations = db.execute("SELECT * FROM course_users WHERE user_id = (SELECT id FROM users WHERE username = '')").fetchall()
    assert len(associations) == 0
    cnt = db.execute("SELECT COUNT(*) FROM course_users").fetchone()[0]
    assert cnt == 7
