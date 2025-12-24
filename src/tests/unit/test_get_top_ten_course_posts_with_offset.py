import models

def test_get_top_ten_course_posts_with_offset1(db):
    models.con = db
    course_id = 1
    offset = 10
    expected_posts = [
        {'title': 'Database Security', 'content': 'Best practices for database security.'},
        {'title': 'Error Handling', 'content': 'Techniques for error handling in code.'},
        {'title': 'Joins in SQL', 'content': 'Different types of joins in SQL.'},
        {'title': 'Debugging Techniques', 'content': 'Effective debugging strategies.'}, 
        {'title': 'Database Backup', 'content': 'Importance of database backups.'}, 
        {'title': 'Pointers in Programming', 'content': 'Understanding pointers.'}, 
        {'title': 'Stored Procedures', 'content': 'Using stored procedures in databases.'},
        {'title': 'Searching Algorithms', 'content': 'Common searching algorithms.'}, 
        {'title': 'Variables and Data Types', 'content': 'Basics of variables and data types.'},
        {'title': 'Database Design', 'content': 'Principles of good database design.'}
    ]
       
    posts = models.get_top_ten_course_posts_with_offset(course_id, offset)
    
    assert posts == expected_posts

def test_get_top_ten_course_posts_with_offset2(db):
    models.con = db
    course_id = 1
    offset = 20
    expected_posts = [{'title': 'Heaps and Priority Queues', 'content': 'Understanding heaps.'}, {'title': 'Loops in Programming', 'content': 'Different types of loops.'}, {'title': 'Views in Databases', 'content': 'Using views effectively.'}, {'title': 'Sorting Techniques', 'content': 'Various sorting techniques explained.'}, {'title': 'Conditionals in Code', 'content': 'Using conditionals effectively.'}]
    posts = models.get_top_ten_course_posts_with_offset(course_id, offset)
    assert posts == expected_posts

def test_get_top_ten_course_posts_with_offset_empty(db):
    models.con = db
    course_id = 2
    offset = 10
    expected_posts = []
    posts = models.get_top_ten_course_posts_with_offset(course_id, offset)
    assert posts == expected_posts
