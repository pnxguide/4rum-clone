import models

def test_get_post_count_by_author_and_course(db):
    models.con = db
    author_username = 'student1'
    course_id = 1
    expected_post_count = 13

    post_count = models.get_post_count_by_author_and_course(author_username, course_id)
    assert post_count == expected_post_count

def test_get_post_count_by_author_and_course_no_posts(db):
    models.con = db
    author_username = 'student2'
    course_id = 3
    expected_post_count = 0

    post_count = models.get_post_count_by_author_and_course(author_username, course_id)
    assert post_count == expected_post_count

def test_get_post_count_by_author_and_course_invalid_user(db):
    models.con = db
    author_username = 'nonexistentuser'
    course_id = 1
    expected_post_count = 0

    post_count = models.get_post_count_by_author_and_course(author_username, course_id)
    assert post_count == expected_post_count

def test_get_post_count_by_author_and_course_invalid_course(db):
    models.con = db
    author_username = 'student1'
    course_id = 999
    expected_post_count = 0

    post_count = models.get_post_count_by_author_and_course(author_username, course_id)
    assert post_count == expected_post_count