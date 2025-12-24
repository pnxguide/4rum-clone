import duckdb

con = duckdb.connect("4rum.db")

con.execute("""
    CREATE SEQUENCE id_sequence_user_types START 1;
    CREATE TABLE user_types (
        id INTEGER PRIMARY KEY DEFAULT nextval('id_sequence_user_types'),
        user_type VARCHAR NOT NULL
    );

    CREATE SEQUENCE id_sequence_courses START 1;
    CREATE TABLE courses (
        id INTEGER PRIMARY KEY DEFAULT nextval('id_sequence_courses'),
        name VARCHAR NOT NULL,
        created_at TIMESTAMP DEFAULT current_timestamp
    );

    CREATE SEQUENCE id_sequence_users START 1;
    CREATE TABLE users (
        id INTEGER PRIMARY KEY DEFAULT nextval('id_sequence_users'),
        username VARCHAR NOT NULL UNIQUE,
        password VARCHAR NOT NULL,
        user_type_id INTEGER NOT NULL,
        FOREIGN KEY (user_type_id) REFERENCES user_types(id)
    );

    CREATE SEQUENCE id_sequence_posts START 1;
    CREATE TABLE posts (
        id INTEGER PRIMARY KEY DEFAULT nextval('id_sequence_posts'),
        title VARCHAR NOT NULL,
        content TEXT NOT NULL,
        author_id INTEGER NOT NULL REFERENCES users(id),
        course_id INTEGER NOT NULL REFERENCES courses(id)
    );

    CREATE TABLE course_users (
        user_id INTEGER NOT NULL REFERENCES users(id),
        course_id INTEGER NOT NULL REFERENCES courses(id),
        PRIMARY KEY (user_id, course_id)
    );
""")

con.execute("""
    INSERT INTO user_types (user_type) 
    VALUES
        ('ADMIN'), ('USER')
""")