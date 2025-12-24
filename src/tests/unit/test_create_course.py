import models

def test_create_course_valid(db):
    models.con = db
    result = models.create_course('Advanced Programming In Practice')
    assert result == True
    course = db.execute("SELECT * FROM courses WHERE name = 'Advanced Programming In Practice'").fetchone()
    assert course is not None
    assert course[1] == 'Advanced Programming In Practice'
    cnt = db.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    assert cnt == 4

def test_create_course_existing_name(db):
    models.con = db
    result = models.create_course('Databases In Practice')
    assert result == False
    courses = db.execute("SELECT * FROM courses WHERE name = 'Databases In Practice'").fetchall()
    assert len(courses) == 1
    cnt = db.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    assert cnt == 3

def test_create_course_empty_name(db):
    models.con = db
    result = models.create_course('')
    assert result == False
    courses = db.execute("SELECT * FROM courses WHERE name = ''").fetchall()
    assert len(courses) == 0
    cnt = db.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    assert cnt == 3

def test_create_course_whitespace_name(db):
    models.con = db
    result = models.create_course('   ')
    assert result == False
    courses = db.execute("SELECT * FROM courses WHERE name = '   '").fetchall()
    assert len(courses) == 0
    cnt = db.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    assert cnt == 3