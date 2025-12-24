import pytest
import duckdb

@pytest.fixture
def db():
    con = duckdb.connect(':memory:')
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
            ('ADMIN'), ('STUDENT')
    """)

    con.execute("""
        INSERT INTO users (username, password, user_type_id) 
        VALUES  
            ('admin', hash('adminpass'), 1), 
            ('student1', hash('studentpass'), 2),
            ('student2', hash('student2pass'), 2),
            ('student3', hash('student3pass'), 2),
    """)

    con.execute("""
        INSERT INTO courses (name) 
        VALUES
            ('Computer Programming 101'),
            ('Databases In Practice'),
            ('Data Structures and Algorithms')
    """)
    
    con.execute("""
        INSERT INTO course_users (user_id, course_id) 
        VALUES
            (2, 1), (2, 2), (2, 3),
            (3, 1), (3, 2),
            (4, 1), (4, 3)
    """)
    
    con.execute("""
        INSERT INTO posts (title, content, author_id, course_id) 
        VALUES  
            ('Welcome to CP101', 'This is the first post in Computer Programming 101.', 2, 1),
            ('Database Basics', 'Let''s discuss the basics of databases.', 2, 2),
            ('Data Structures Overview', 'An overview of data structures.', 2, 3),
            ('Arrays and Lists', 'Discussion about arrays and lists.', 3, 1),
            ('SQL Queries', 'How to write SQL queries.', 3, 1),
            ('Sorting Algorithms', 'Let''s talk about sorting algorithms.', 3, 2),
            ('Trees and Graphs', 'Understanding trees and graphs.', 4, 3),
            ('Functions in Programming', 'Discussion on functions and their uses.', 2, 1),
            ('Normalization in Databases', 'Why normalization is important.', 2, 1),
            ('Linked Lists', 'Deep dive into linked lists.', 2, 1),
            ('Control Structures', 'If-else, loops, and more.', 2, 1),
            ('Indexes in Databases', 'How indexes improve performance.', 3, 1),
            ('Hash Tables', 'Understanding hash tables.', 4, 3),
            ('Object-Oriented Programming', 'Basics of OOP.', 2, 1),
            ('Transactions in Databases', 'ACID properties and transactions.', 3, 2),
            ('Graphs Algorithms', 'Exploring algorithms on graphs.', 4, 3),
            ('Recursion', 'Understanding recursion in programming.', 2, 1),
            ('Database Security', 'Best practices for database security.', 3, 1),
            ('Dynamic Programming', 'An introduction to dynamic programming.', 4, 3),
            ('Error Handling', 'Techniques for error handling in code.', 2, 1),
            ('Joins in SQL', 'Different types of joins in SQL.', 3, 1),
            ('Stacks and Queues', 'Understanding stacks and queues.', 4, 3),
            ('Debugging Techniques', 'Effective debugging strategies.', 2, 1),
            ('Database Backup', 'Importance of database backups.', 3, 1),
            ('Algorithm Complexity', 'Big O notation and complexity analysis.', 4, 3),
            ('Pointers in Programming', 'Understanding pointers.', 2, 1),
            ('Stored Procedures', 'Using stored procedures in databases.', 3, 1),
            ('Searching Algorithms', 'Common searching algorithms.', 3, 1),
            ('Variables and Data Types', 'Basics of variables and data types.', 2, 1),
            ('Database Design', 'Principles of good database design.', 3, 1),
            ('Heaps and Priority Queues', 'Understanding heaps.', 3, 1),
            ('Loops in Programming', 'Different types of loops.', 2, 1),
            ('Views in Databases', 'Using views effectively.', 3, 1),
            ('Sorting Techniques', 'Various sorting techniques explained.', 3, 1),
            ('Conditionals in Code', 'Using conditionals effectively.', 2, 1)
    """)

    yield con
    con.close()
