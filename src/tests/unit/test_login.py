import models

def test_login_valid(db):
    models.con = db
    user_type = models.login('student1', 'studentpass')
    assert user_type == 'STUDENT'

def test_login_invalid_username(db):
    models.con = db
    user_type = models.login('nonexistentuser', 'somepass')
    assert user_type == False

def test_login_invalid_password(db):
    models.con = db
    user_type = models.login('student1', 'wrongpass')
    assert user_type == False

def test_login_empty_username(db):
    models.con = db
    user_type = models.login('', 'somepass')
    assert user_type == False

def test_login_empty_password(db):
    models.con = db
    user_type = models.login('student1', '')
    assert user_type == False

def test_login_empty_input(db):
    models.con = db
    user_type = models.login('', '')
    assert user_type == False