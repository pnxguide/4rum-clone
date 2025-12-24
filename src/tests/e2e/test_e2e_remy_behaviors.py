import models

def test_e2e_remy_behaviors(db):
    models.con = db

    # Step 1: Admin create a course
    result = models.create_course('Ratatouille Course')
    assert result == True
    assert db.execute("SELECT * FROM courses WHERE name = ?", ['Ratatouille Course']).fetchone() is not None
    assert db.execute("SELECT COUNT(*) FROM courses").fetchone()[0] >= 1
    assert db.execute("SELECT name FROM courses WHERE name = ?", ['Ratatouille Course']).fetchone()[0] == 'Ratatouille Course'

    # Step 2: Remy registers and logs in
    result = models.register('remy', 'remy_hashed_pw')
    assert result == True
    assert db.execute("SELECT * FROM users WHERE username = ?", ['remy']).fetchone() is not None
    user_type = models.login('remy', 'remy_hashed_pw')
    assert user_type == 'STUDENT'

    # Step 3: Remy Checks courses before joining
    courses = models.get_all_courses_by_user('remy')
    assert len(courses) == 0

    # Step 4: Admin adds Remy to the course
    course = db.execute("SELECT id FROM courses WHERE name = ?", ['Ratatouille Course']).fetchone()
    result = models.add_user_to_course('remy', course[0])
    assert result == True
    assert db.execute("SELECT * FROM course_users WHERE user_id = (SELECT id FROM users WHERE username = ?) AND course_id = ?", ['remy', course[0]]).fetchone() is not None
    assert db.execute("SELECT COUNT(*) FROM course_users WHERE course_id = ?", [course[0]]).fetchone()[0] == 1

    # Step 5: Remy Checks courses after joining
    courses = models.get_all_courses_by_user('remy')
    assert len(courses) == 1
    assert courses[0]['course_name'] == 'Ratatouille Course'

    # Step pre 6: Setting up authors create posts in the course
    indy = 'Indy'
    result = models.register(indy, 'indy_hashed_pw')
    assert result == True
    assert db.execute("SELECT * FROM users WHERE username = ?", [indy]).fetchone() is not None
    result = models.add_user_to_course(indy, course[0])
    assert result == True
    assert db.execute("SELECT * FROM course_users WHERE user_id = (SELECT id FROM users WHERE username = ?) AND course_id = ?", [indy, course[0]]).fetchone() is not None
    assert db.execute("SELECT COUNT(*) FROM course_users WHERE course_id = ?", [course[0]]).fetchone()[0] == 2

    # Step pre pre 6: Admin check dashboard before posts
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
        },
        {
            "course_name": "Ratatouille Course",
            "user_count": 2,
            "post_count": 0
        }
    ]
    for iter in range(len(user_cnt_in_courses)):
        assert user_cnt_in_courses[iter]["course_name"] == expected_user_post_counts[iter]["course_name"]
        assert user_cnt_in_courses[iter]['user_count'] == expected_user_post_counts[iter]['user_count']
        assert user_cnt_in_courses[iter]['post_count'] == expected_user_post_counts[iter]['post_count']
    
    result = models.create_course_post(course[0], 'How can i solve this SP', 'I need help with solving this SP', indy)
    assert result == True
    result = models.create_course_post(course[0], 'Best way to learn AI', 'What is the best way to learn AI?', indy)
    assert result == True
    result = models.create_course_post(course[0], 'Hey Bro,Now I haved solve this SP ','I just copy the instructions to CHATGPT and wow it make everything easier, I mean it do this SP for me', indy) 
    assert result == True

    # Step pre pre 6: Admin check dashboard after posts
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
        },
        {
            "course_name": "Ratatouille Course",
            "user_count": 2,
            "post_count": 3
        }
    ]
    for iter in range(len(user_cnt_in_courses)):
        assert user_cnt_in_courses[iter]["course_name"] == expected_user_post_counts[iter]["course_name"]
        assert user_cnt_in_courses[iter]['user_count'] == expected_user_post_counts[iter]['user_count']
        assert user_cnt_in_courses[iter]['post_count'] == expected_user_post_counts[iter]['post_count']

    # Step 6: Remy view posts in course
    count = models.get_post_count_by_course(course[0])
    assert count == 3
    posts = models.get_top_ten_course_posts_with_offset(course[0], 0)
    assert len(posts) == 3
    titles = [p['title'] for p in posts]
    assert 'How can i solve this SP' in titles
    assert 'Best way to learn AI' in titles
    assert 'Hey Bro,Now I haved solve this SP ' in titles

    # Step 7: Remy try to select Edit his post
    posts_by_remy = models.get_posts_by_author_and_course('remy', course[0], 0)
    assert posts_by_remy is None or len(posts_by_remy) == 0

    # Step pre 8: Setting up pagination posts with story-driven titles
    story_posts = [
        ("Post 1: Setting up the SP", "Starting with requirements and environment setup: duckdb + pytest."),
        ("Post 2: Stuck on foreign keys", "FK constraints caused insert errors — has anyone seen this?"),
        ("Post 3: Basic queries working", "Verified initial data in users/courses/posts and tested LIMIT/OFFSET."),
        ("Post 4: Login flow passes", "Hashed passwords; user_type resolves to STUDENT. Login OK."),
        ("Post 5: Joined the course", "add_user_to_course succeeded; get_all_courses_by_user shows membership."),
        ("Post 6: First post created", "create_course_post works; course post count increased as expected."),
        ("Post 7: Edited my post", "Updated title/content and verified via get_posts_by_author_and_course."),
        ("Post 8: Deleted a post", "Removed a redundant post; course count decreased correctly."),
        ("Post 9: Wrap-up and tips", "Recommend integration tests covering create→read→update→delete lifecycle."),
    ]
    for title, content in story_posts:
        result = models.create_course_post(course[0], title, content, indy)
        assert result == True

    # Step 8: Remy test pagination
    batch1 = models.get_top_ten_course_posts_with_offset(course[0], 0)
    batch2 = models.get_top_ten_course_posts_with_offset(course[0], 10)
    assert len(batch1) == 10
    assert len(batch2) == 2
    titles_batch1 = [p['title'] for p in batch1]
    titles_batch2 = [p['title'] for p in batch2]
    assert not any(title in titles_batch1 for title in titles_batch2)

    # Step 9: Remy create his own post
    result = models.create_course_post(course[0], 'Remy\'s Culinary Post', 'Exploring the art of cooking while coding.', 'remy')
    assert result == True
    assert db.execute("SELECT * FROM posts WHERE title = ? AND author_id = (SELECT id FROM users WHERE username = ?)", ['Remy\'s Culinary Post', 'remy']).fetchone() is not None
    assert db.execute("SELECT COUNT(*) FROM posts WHERE course_id = ?", [course[0]]).fetchone()[0] == 13
    result = models.create_course_post(course[0], 'I\'m struggling with this SP', 'I\'m having trouble balancing flavors and functions.', 'remy')
    assert result == True
    assert db.execute("SELECT * FROM posts WHERE title = ? AND author_id = (SELECT id FROM users WHERE username = ?)", ['I\'m struggling with this SP', 'remy']).fetchone() is not None
    assert db.execute("SELECT COUNT(*) FROM posts WHERE course_id = ?", [course[0]]).fetchone()[0] == 14

    # Step pre 10: Admin check dashboard after Remy posts
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
        },
        {
            "course_name": "Ratatouille Course",
            "user_count": 2,
            "post_count": 14
        }
    ]
    for iter in range(len(user_cnt_in_courses)):
        assert user_cnt_in_courses[iter]["course_name"] == expected_user_post_counts[iter]["course_name"]
        assert user_cnt_in_courses[iter]['user_count'] == expected_user_post_counts[iter]['user_count']
        assert user_cnt_in_courses[iter]['post_count'] == expected_user_post_counts[iter]['post_count'] 
    # Step 10: Remy try Edit his post
    posts_cnt = models.get_post_count_by_author_and_course('remy', course[0])
    assert posts_cnt == 2
    posts_by_remy = models.get_posts_by_author_and_course('remy', course[0], 0)
    assert len(posts_by_remy) == 2
    post_to_edit = posts_by_remy[1]['post_id']
    new_title = "EDITED: struggling with this SP"
    new_content = "Finding the right balance between flavors and functions is tough! it is really hard."
    result = models.update_post(post_to_edit, new_title, new_content)

    # Step 11: Remy wants to delete a post
    posts_by_remy = models.get_posts_by_author_and_course('remy', course[0], 0)
    post_to_delete = posts_by_remy[0]['post_id']
    result = models.delete_post(post_to_delete)
    assert result == True