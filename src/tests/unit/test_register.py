import models

def test_register_valid(db):
    models.con = db
    result = models.register('newuser', 'newpass')
    assert result == True
    user = db.execute("SELECT * FROM users WHERE username = 'newuser'").fetchone()
    assert user is not None
    assert user[1] == 'newuser'
    assert user[2] == f'{db.execute("SELECT hash('newpass')").fetchone()[0]}'
    user_type = db.execute("SELECT user_type FROM user_types WHERE id = ?", [user[3]]).fetchone()[0]
    assert (user[3] == 2 or user_type == "STUDENT")
    cnt = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    assert cnt == 5

def test_register_existing_username(db):
    models.con = db
    result = models.register('student1', 'anotherpass')
    assert result == False
    users = db.execute("SELECT * FROM users WHERE username = 'student1'").fetchall()
    assert len(users) == 1
    cnt = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    assert cnt == 4

def test_register_empty_input(db):
    models.con = db
    result = models.register('', '')
    assert result == False
    users = db.execute("SELECT * FROM users WHERE username = ''").fetchall()
    assert len(users) == 0
    cnt = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    assert cnt == 4

def test_register_empty_password(db):
    models.con = db
    result = models.register('userwithnopass', '')
    assert result == False
    users = db.execute("SELECT * FROM users WHERE username = 'userwithnopass'").fetchall()
    assert len(users) == 0
    cnt = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    assert cnt == 4

def test_register_empty_username(db):
    models.con = db
    result = models.register('', 'somepass')
    assert result == False
    users = db.execute("SELECT * FROM users WHERE username = 'userwithnopass'").fetchall()
    assert len(users) == 0
    cnt = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    assert cnt == 4

