import duckdb

con = duckdb.connect("4rum.db")

"""
Unauthenticated User Feature
"""

def register(username: str, password: str):
    pass

def login(username: str, password: str):
    pass

"""
Student Feature
"""

def get_all_courses_by_user(username: str):
    pass

def get_post_count_by_course(course_id: int):
    pass

def get_top_ten_course_posts_with_offset(course_id: int, offset: int):
    pass

def create_course_post(course_id: int, title: str, content: str, author_username: str):
    pass

def get_post_count_by_author_and_course(author_username: str, course_id: int):
    pass

def get_posts_by_author_and_course(username: str, course_id: int, offset: int):
    pass

def update_post(post_id: int, title: str, content: str):
    pass

def delete_post(post_id: int):
    pass

"""
Admin Feature
"""

def create_course(course_name: str):
    pass

def add_user_to_course(username: str, course_id: int):
    pass

def get_users_and_post_count_in_course():
    pass
