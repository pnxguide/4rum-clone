import models

def test_user_post_workflow_complete(db):
    models.con = db
    course_id = 1
    username = 'student1'
    
    result = models.create_course_post(course_id, 'Integration Test Post', 'Original Content', username)
    assert result == True
    
    count = models.get_post_count_by_course(course_id)
    assert count > 0
    
    posts = models.get_posts_by_author_and_course(username, course_id, 0)
    assert posts is not None
    post_id = posts[-1]['post_id']
    
    result = models.update_post(post_id, 'Updated Title', 'Updated Content')
    assert result == True
    
    posts = models.get_posts_by_author_and_course(username, course_id, 0)
    assert any(p['post_id'] == post_id and p['title'] == 'Updated Title' for p in posts)
    
    result = models.delete_post(post_id)
    assert result == True


def test_multiple_users_posting_in_course(db):
    models.con = db
    course_id = 1
    
    initial_count = models.get_post_count_by_course(course_id)
    
    users = ['student1', 'student2', 'student3']
    for i, user in enumerate(users):
        result = models.create_course_post(course_id, f'Post by {user}', f'Content {i}', user)
        assert result == True
    
    new_count = models.get_post_count_by_course(course_id)
    assert new_count == initial_count + 3
    
    for user in users:
        cnt = models.get_post_count_by_author_and_course(user, course_id)
        print(f"Post count for {user}: {cnt}")
        posts = []
        iter = 0
        while iter * 10 < cnt:
            post = models.get_posts_by_author_and_course(user, course_id, iter * 10)
            posts = posts + post if post else posts
            iter += 1
        print(post)
        assert posts is not None
        assert user in [p['title'].split(' by ')[1] for p in posts if 'by' in p["title"]]


def test_user_posting_across_multiple_courses(db):
    models.con = db
    username = 'student1'
    courses = [1, 2, 3]
    
    initial_counts = {c: models.get_post_count_by_author_and_course(username, c) for c in courses}
    
    for course_id in courses:
        result = models.create_course_post(course_id, f'Post in Course {course_id}', 'Content', username)
        assert result == True
    
    for course_id in courses:
        count = models.get_post_count_by_author_and_course(username, course_id)
        assert count == initial_counts[course_id] + 1


def test_pagination_workflow(db):
    models.con = db
    course_id = 1
    
    for i in range(15):
        models.create_course_post(course_id, f'Post {i}', f'Content {i}', 'student1')
    
    batch1 = models.get_top_ten_course_posts_with_offset(course_id, 0)
    assert len(batch1) <= 10
    assert len(batch1) > 0
    
    batch2 = models.get_top_ten_course_posts_with_offset(course_id, 10)
    if len(batch1) == 10 and len(batch2) > 0:
        assert batch1[0]['title'] != batch2[0]['title']


def test_post_validation_workflow(db):
    models.con = db
    
    result = models.create_course_post(999, 'Title', 'Content', 'student1')
    assert result == False
    
    result = models.create_course_post(1, 'Title', 'Content', 'nonexistent_user')
    assert result == False
    
    models.create_course_post(1, 'Title', 'Content', 'student1')
    posts = models.get_posts_by_author_and_course('student1', 1, 0)
    post_id = posts[-1]['post_id']
    
    result = models.update_post(post_id, '', 'Content')
    assert result == False
    
    result = models.update_post(post_id, 'Title', '')
    assert result == False
    
    result = models.update_post(999, 'Title', 'Content')
    assert result == False
    
    result = models.delete_post(999)
    assert result == False


def test_content_retrieval_workflow(db):
    models.con = db
    username = 'student1'
    course_id = 2
    
    post_titles = ['First Post', 'Second Post', 'Third Post']
    for title in post_titles:
        models.create_course_post(course_id, title, f'Content of {title}', username)
    
    posts = models.get_posts_by_author_and_course(username, course_id, 0)
    assert posts is not None
    retrieved_titles = [p['title'] for p in posts]
    
    for title in post_titles:
        assert title in retrieved_titles
    
    all_posts = models.get_top_ten_course_posts_with_offset(course_id, 0)
    assert len(all_posts) > 0
