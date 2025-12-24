import models

def test_create_course_post_valid(db):
    models.con = db
    course_id = 1
    title = 'New Post Title'
    content = 'This is the content of the new post.'
    author_username = 'student1'
    result = models.create_course_post(course_id, title, content, author_username)
    assert result == True
    post = db.execute("""
        SELECT p.title, p.content, u.username 
        FROM posts p
        INNER JOIN users u ON p.author_id = u.id
        WHERE p.title = ? AND p.content = ? AND u.username = ?
    """, [title, content, author_username]).fetchone()
    assert post is not None
    assert post[0] == title
    assert post[1] == content
    assert post[2] == author_username
    post_count = db.execute("SELECT COUNT(*) FROM posts WHERE course_id = ?", [course_id]).fetchone()[0]
    assert post_count == 26

def test_create_course_post_invalid_course(db):
    models.con = db
    course_id = 999 
    title = 'Invalid Course Post'
    content = 'This post should not be created.'
    author_username = 'student1'
    result = models.create_course_post(course_id, title, content, author_username)
    assert result == False
    post = db.execute("""
        SELECT * FROM posts 
        WHERE title = ? AND content = ?
    """, [title, content]).fetchone()
    assert post is None

def test_create_course_post_invalid_user(db):
    models.con = db
    course_id = 1
    title = 'Invalid User Post'
    content = 'This post should not be created.'
    author_username = 'nonexistentuser'
    result = models.create_course_post(course_id, title, content, author_username)
    assert result == False
    post = db.execute("""
        SELECT * FROM posts 
        WHERE title = ? AND content = ?
    """, [title, content]).fetchone()
    post_count = db.execute("SELECT COUNT(*) FROM posts WHERE course_id = ?", [course_id]).fetchone()[0]
    assert post_count == 25

def test_create_course_post_duplicate_title(db):
    models.con = db
    course_id = 1
    title = 'Welcome to CP101'
    content = 'This is another post with a duplicate title.'
    author_username = 'student1'
    result = models.create_course_post(course_id, title, content, author_username)
    assert result == True
    posts = db.execute("""
        SELECT * FROM posts 
        WHERE title = ? AND content = ?
    """, [title, content]).fetchall()
    assert len(posts) == 1
    post_count = db.execute("SELECT COUNT(*) FROM posts WHERE course_id = ?", [course_id]).fetchone()[0]
    assert post_count == 26
