import models

def test_get_posts_by_author_and_course(db):
    models.con = db
    author_username = 'student1'
    course_id = 1
    expected_posts = [{'post_id': 1, 'title': 'Welcome to CP101', 'content': 'This is the first post in Computer Programming 101.'}, {'post_id': 8, 'title': 'Functions in Programming', 'content': 'Discussion on functions and their uses.'}, {'post_id': 9, 'title': 'Normalization in Databases', 'content': 'Why normalization is important.'}, {'post_id': 10, 'title': 'Linked Lists', 'content': 'Deep dive into linked lists.'}, {'post_id': 11, 'title': 'Control Structures', 'content': 'If-else, loops, and more.'}, {'post_id': 14, 'title': 'Object-Oriented Programming', 'content': 'Basics of OOP.'}, {'post_id': 17, 'title': 'Recursion', 'content': 'Understanding recursion in programming.'}, {'post_id': 20, 'title': 'Error Handling', 'content': 'Techniques for error handling in code.'}, {'post_id': 23, 'title': 'Debugging Techniques', 'content': 'Effective debugging strategies.'}, {'post_id': 26, 'title': 'Pointers in Programming', 'content': 'Understanding pointers.'}]

    posts = models.get_posts_by_author_and_course(author_username, course_id, 0)
    assert posts == expected_posts

def test_get_posts_by_author_and_course_no_posts(db):
    models.con = db
    author_username = 'student2'
    course_id = 3

    posts = models.get_posts_by_author_and_course(author_username, course_id, 0)
    assert posts is None

def test_get_posts_by_author_and_course_invalid_user(db):
    models.con = db
    author_username = 'nonexistentuser'
    course_id = 1

    posts = models.get_posts_by_author_and_course(author_username, course_id, 0)
    assert posts is None

def test_get_posts_by_author_and_course_invalid_course(db):
    models.con = db
    author_username = 'student1'
    course_id = 999

    posts = models.get_posts_by_author_and_course(author_username, course_id, 0)
    assert posts is None