import models

def test_add_course_get_dashboard_valid(db):
    models.con = db

    models.create_course('Computer Game Development')
    models.create_course('Operating Systems')
    
    user_cnt_in_courses = models.get_users_and_post_count_in_course()
    
    expected_user_post_counts = [
        {
            "course_name": "Computer Game Development",
            "user_count": 0,
            "post_count": 0
        },
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
        },
        {
            "course_name": "Operating Systems",
            "user_count": 0,
            "post_count": 0
        }
    ]
    for iter in range(len(user_cnt_in_courses)):
        assert user_cnt_in_courses[iter]["course_name"] == expected_user_post_counts[iter]["course_name"]
        assert user_cnt_in_courses[iter]['user_count'] == expected_user_post_counts[iter]['user_count']
        assert user_cnt_in_courses[iter]['post_count'] == expected_user_post_counts[iter]['post_count']

def test_add_user_to_course_get_dashboard_valid(db):
    models.con = db

    models.add_user_to_course('student2', 3)
    models.add_user_to_course('student3', 2)

    user_cnt_in_courses = models.get_users_and_post_count_in_course()
    
    expected_user_post_counts = [
        {
            "course_name": "Computer Programming 101",
            "user_count": 3,
            "post_count": 25
        },
        {
            "course_name": "Data Structures and Algorithms",
            "user_count": 3,
            "post_count": 7
        },
        {
            "course_name": "Databases In Practice",
            "user_count": 3,
            "post_count": 3
        }
    ]
    for iter in range(len(user_cnt_in_courses)):
        assert user_cnt_in_courses[iter]["course_name"] == expected_user_post_counts[iter]["course_name"]
        assert user_cnt_in_courses[iter]['user_count'] == expected_user_post_counts[iter]['user_count']
        assert user_cnt_in_courses[iter]['post_count'] == expected_user_post_counts[iter]['post_count']

def test_create_course_post_get_dashboard_valid(db):
    models.con = db

    models.create_course_post(1, 'New Post 1', 'Content for new post 1', 'student1')
    models.create_course_post(2, 'New Post 2', 'Content for new post 2', 'student1')
    models.create_course_post(3, 'New Post 3', 'Content for new post 3', 'student1')

    user_cnt_in_courses = models.get_users_and_post_count_in_course()
    
    expected_user_post_counts = [
        {
            "course_name": "Computer Programming 101",
            "user_count": 3,
            "post_count": 26
        },
        {
            "course_name": "Data Structures and Algorithms",
            "user_count": 2,
            "post_count": 8
        },
        {
            "course_name": "Databases In Practice",
            "user_count": 2,
            "post_count": 4
        }
    ]
    for iter in range(len(user_cnt_in_courses)):
        assert user_cnt_in_courses[iter]["course_name"] == expected_user_post_counts[iter]["course_name"]
        assert user_cnt_in_courses[iter]['user_count'] == expected_user_post_counts[iter]['user_count']
        assert user_cnt_in_courses[iter]['post_count'] == expected_user_post_counts[iter]['post_count']

def test_delete_post_get_dashboard_valid(db):
    models.con = db

    models.delete_post(1)
    models.delete_post(2)
    models.delete_post(3)

    user_cnt_in_courses = models.get_users_and_post_count_in_course()
    
    expected_user_post_counts = [
        {
            "course_name": "Computer Programming 101",
            "user_count": 3,
            "post_count": 24
        },
        {
            "course_name": "Data Structures and Algorithms",
            "user_count": 2,
            "post_count": 6
        },
        {
            "course_name": "Databases In Practice",
            "user_count": 2,
            "post_count": 2
        }
    ]
    for iter in range(len(user_cnt_in_courses)):
        assert user_cnt_in_courses[iter]["course_name"] == expected_user_post_counts[iter]["course_name"]
        assert user_cnt_in_courses[iter]['user_count'] == expected_user_post_counts[iter]['user_count']
        assert user_cnt_in_courses[iter]['post_count'] == expected_user_post_counts[iter]['post_count']

def test_update_post_get_dashboard_valid(db):
    models.con = db

    models.update_post(4, 'Updated Post Title', 'Updated content for post 4')

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
