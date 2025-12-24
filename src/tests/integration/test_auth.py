import models

def test_register_login_valid(db):
    models.con = db
    username = 'newuser'
    password = 'newpass'
    register_result = models.register(username, password)
    assert register_result == True

    user_type = models.login(username, password)
    assert user_type == 'STUDENT'

def test_multiple_register_login_valid(db):
    models.con = db
    for i in range(10):
        username = f'user{i}'
        password = f'pass{i}'
        register_result = models.register(username, password)
        assert register_result == True

        user_type = models.login(username, password)
        assert user_type == 'STUDENT'

def test_register_login_wrong_password(db):
    models.con = db
    username = 'student5'
    password = 'pass'
    result = models.register(username, password)
    assert result == True
    wrong_password = 'incorrectpass'
    user_type = models.login(username, wrong_password)
    assert user_type == False

def test_login_registered_user_types(db):
    models.con = db
    admin_username = 'adminuser'
    admin_password = 'adminpass'
    student_username = 'studentuser'
    student_password = 'studentpass'

    admin_register_result = models.register(admin_username, admin_password)
    assert admin_register_result == True
    student_register_result = models.register(student_username, student_password)
    assert student_register_result == True
    admin_user_type = models.login(admin_username, admin_password)
    assert admin_user_type == 'STUDENT'
    student_user_type = models.login(student_username, student_password)
    assert student_user_type == 'STUDENT'
    
def test_login_nonexistent_register_login_user(db):
    models.con = db
    username = 'nonexistentuser'
    password = 'somepass'
    user_type = models.login(username, password)
    assert user_type == False
    register_result = models.register(username, password)
    assert register_result == True
    user_type_after_register = models.login(username, password)
    assert user_type_after_register == 'STUDENT'