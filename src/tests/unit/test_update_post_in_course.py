import models

def test_update_post_valid(db):
    models.con = db
    post_id = 1
    new_title = "Updated Title"
    new_content = "Updated content for the post."
    result = models.update_post(post_id, new_title, new_content)
    assert result == True
    post = db.execute("SELECT title, content FROM posts WHERE id = ?", [post_id]).fetchone()
    assert post is not None
    assert post[0] == new_title
    assert post[1] == new_content

def test_update_post_nonexistent_post(db):
    models.con = db
    post_id = 999
    new_title = "New Title"
    new_content = "New content."
    result = models.update_post(post_id, new_title, new_content)
    assert result == False

def test_update_post_empty_title(db):
    models.con = db
    post_id = 1
    new_title = ""
    new_content = "Content with empty title."
    result = models.update_post(post_id, new_title, new_content)
    assert result == False

def test_update_post_empty_content(db):
    models.con = db
    post_id = 1
    new_title = "Title with empty content"
    new_content = ""
    result = models.update_post(post_id, new_title, new_content)
    assert result == False

def test_update_post_empty_input(db):
    models.con = db
    post_id = 1
    new_title = ""
    new_content = ""
    result = models.update_post(post_id, new_title, new_content)
    assert result == False

def test_update_post_invalid_id(db):
    models.con = db
    post_id = -1
    new_title = "Title"
    new_content = "Content."
    result = models.update_post(post_id, new_title, new_content)
    assert result == False
