import models

def test_dashboard(db):
    models.con = db
    user_cnt_in_courses = models.get_users_and_post_count_in_course()
    
    expected_user_post_counts = [
        {
            "course_name": "Computer Programming 101",
            "user_count": 3,
            "post_count": 25
        },
        {
            "course_name": "Data Structures and Algorithms",
            "user_count": 2,
            "post_count": 7
        },
        {
            "course_name": "Databases In Practice",
            "user_count": 2,
            "post_count": 3
        }
    ]
    for iter in range(len(user_cnt_in_courses)):
        assert user_cnt_in_courses[iter]["course_name"] == expected_user_post_counts[iter]["course_name"]
        assert user_cnt_in_courses[iter]['user_count'] == expected_user_post_counts[iter]['user_count']
        assert user_cnt_in_courses[iter]['post_count'] == expected_user_post_counts[iter]['post_count']

def test_delete_course_get_dashboard_no_courses(db):
    models.con = db

    db.execute("DELETE FROM course_users")
    db.execute("DELETE FROM posts")
    db.execute("DELETE FROM courses")

    user_cnt_in_courses = models.get_users_and_post_count_in_course()
    for iter in range(len(user_cnt_in_courses)):
        assert user_cnt_in_courses[iter]["course_name"] == None
        assert user_cnt_in_courses[iter]['user_count'] == 0
        assert user_cnt_in_courses[iter]['post_count'] == 0
    assert len(user_cnt_in_courses) == 0