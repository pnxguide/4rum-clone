import models

def test_delete_post_valid(db):
    models.con = db
    post_id_to_delete = 1
    result = models.delete_post(post_id_to_delete)
    assert result == True
    post = db.execute("SELECT * FROM posts WHERE id = ?", [post_id_to_delete]).fetchone()
    assert post is None

def test_delete_post_nonexistent(db):
    models.con = db
    post_id_to_delete = 999 
    result = models.delete_post(post_id_to_delete)
    assert result == False
    cnt = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    assert cnt == 35  

def test_delete_post_invalid_id(db):
    models.con = db
    post_id_to_delete = -1 
    result = models.delete_post(post_id_to_delete)
    assert result == False
    cnt = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    assert cnt == 35 