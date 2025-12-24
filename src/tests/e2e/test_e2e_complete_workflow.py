import models

def test_e2e_complete_forum_workflow(db):
    models.con = db
    # Step 1: Admin creates multiple courses
    courses_name = ['Course A', 'Course B', 'Course C']
    for name in courses_name:
        result = models.create_course(name)
        assert result == True

    # Verify courses created
    for name in courses_name:
        courses = db.execute("SELECT * FROM courses WHERE name = ?", [name]).fetchall()
        assert len(courses) == 1

    # Step 2: Register students
    students = ['student9', 'student99', 'student999']
    for student in students:
        result = models.register(student, 'hashed_pw')
        assert result == True

    # Step 3: Login students
    for student in students:
        user_type = models.login(student, 'hashed_pw')
        assert user_type == 'STUDENT'

    # Check user courses before joining
    for student in students:
        courses = models.get_all_courses_by_user(student)
        assert len(courses) == 0

    # Step 4: Students join courses
    for student in students:
        for name in courses_name:
            course = db.execute("SELECT id FROM courses WHERE name = ?", [name]).fetchone()
            result = models.add_user_to_course(student, course[0])
            assert result == True

    # Verify students joined courses
    for student in students:
        courses = models.get_all_courses_by_user(student)
        assert len(courses) == len(courses_name)

    # Step 5: Students create posts in courses
    for student in students:
        for name in courses_name:
            course = db.execute("SELECT id FROM courses WHERE name = ?", [name]).fetchone()
            for i in range(3):
                title = f"{student} Post {i+1} in {name}"
                content = f"Content for {title}"
                result = models.create_course_post(course[0], title, content, student)
                assert result == True
    # Verify posts created
    for student in students:
        for name in courses_name:
            course = db.execute("SELECT id FROM courses WHERE name = ?", [name]).fetchone()
            count = models.get_post_count_by_author_and_course(student, course[0])
            assert count == 3

    # Step 6: Students retrieve and verify their posts
    for student in students:
        for name in courses_name:
            course = db.execute("SELECT id FROM courses WHERE name = ?", [name]).fetchone()
            posts = models.get_posts_by_author_and_course(student, course[0], 0)
            assert len(posts) == 3
            for i in range(3):
                expected_title = f"{student} Post {i+1} in {name}"
                assert any(p['title'] == expected_title for p in posts)


    # Step 7: Students create more posts to test pagination
    for student in students:
        for name in courses_name:
            course = db.execute("SELECT id FROM courses WHERE name = ?", [name]).fetchone()
            for i in range(100):  # Create 100 more posts
                title = f"{student} Extra Post {i+1} in {name}"
                content = f"Content for {title}"
                result = models.create_course_post(course[0], title, content, student)
                assert result == True

    # Step 8: Students retrieve posts with pagination
    for student in students:
        for name in courses_name:
            course = db.execute("SELECT id FROM courses WHERE name = ?", [name]).fetchone()
            batch1 = models.get_top_ten_course_posts_with_offset(course[0], 0)
            batch2 = models.get_top_ten_course_posts_with_offset(course[0], 10)
            assert len(batch1) <= 10
            assert len(batch2) <= 10
            if len(batch1) == 10 and len(batch2) > 0:
                titles_batch1 = [p['title'] for p in batch1]
                titles_batch2 = [p['title'] for p in batch2]
                assert not any(title in titles_batch1 for title in titles_batch2)

    # Step 9: Students edit
    for student in students:
        for name in courses_name:
            course = db.execute("SELECT id FROM courses WHERE name = ?", [name]).fetchone()
            posts = models.get_posts_by_author_and_course(student, course[0], 0)
            post_to_edit = posts[0]['post_id']
            new_title = f"EDITED: {posts[0]['title']}"
            new_content = f"Updated content for {new_title}"
            result = models.update_post(post_to_edit, new_title, new_content)
            assert result == True

            # Verify edit
            updated_posts = models.get_posts_by_author_and_course(student, course[0], 0)
            assert any(p['post_id'] == post_to_edit and p['title'] == new_title for p in updated_posts)

    # Step 10: Students delete a post
    for student in students:
        for name in courses_name:
            course = db.execute("SELECT id FROM courses WHERE name = ?", [name]).fetchone()
            posts = models.get_posts_by_author_and_course(student, course[0], 0)
            post_to_delete = posts[1]['post_id']
            count_before = models.get_post_count_by_course(course[0])

            result = models.delete_post(post_to_delete)
            assert result == True

            # Verify deletion
            count_after = models.get_post_count_by_course(course[0])
            assert count_after == count_before - 1
