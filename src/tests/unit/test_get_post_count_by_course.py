import models

def test_get_post_count_by_course(db):
    models.con = db
    course_id = 1
    expected_post_count = 25 
    post_count = models.get_post_count_by_course(course_id)
    assert post_count == expected_post_count
