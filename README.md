# Solo Project #2 - 4rum Clone

In this project, you will build an offline [4rum](https://4rum.poomzi.com). Since you only have several weeks, we do not expect you to build a fully functional system. Still, you need to implement the key functionalities as follows:

- Registration
- Authentication
- Authorization
- Course Management
- Post Management

All of the application data must be persisted through [DuckDB](https://duckdb.org/).

> 🐥 You do not need to implement a web or a mobile application with a fancy interface. We only want a CLI-style interface.

> 🐥 You really need to focus on this solo project since it will be a baseline for your team project in the future.

## Getting Started

First, you use this template to create your private GitHub repository.

> 🐥 Your repository must be private. Otherwise, you are committing plagiarism implicitly.

All you need to do is to **modify the only file, `models.py`**, to make it satisfy the requirements.

> 🐥 When autograding, we will only copy your `models.py` to the autograder. Please only work on that file.

### Database Definition

In this task, we have already designed and defined the database schema for this application. The definition is as the following SQL statements:

```sql
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
```

> 🐥 You may want to read more about `SEQUENCE` and `nextval` constructs. Fundamentally, they are used for making the column be *autoincremented*.

We also initialized some important master data (i.e., data about the entity) as follows:

```sql
INSERT INTO user_types (user_type) 
    VALUES
        ('ADMIN'), ('STUDENT')
```

All of these statements are in `create_schema.py`. That is, you only need to run this file using the following command:

```
python3 create_schema.py
```

After running it, it will create `4rum.db` file, which is your database file. This file contains all the definitions, tables, and rows.

> 🐥 You only need to run it for the first time.

> 🐥 If you would like to reset the database, you can delete `4rum.db` and rerun `create_schema.py`

### Running the Application

Please try understanding `run.py` and `views.py` carefully. `run.py` is the driver file for this application. This means, to run this application, you need to run this file, as follows:

```python
python3 run.py
```

> 🐥 Again, all your implementations must be in `src/models.py`.

## Feature Set 1 - Unauthenticated Users

### Feature #1 - Student Registration

Unregistered students must be able to register their identities (i.e., username and password) to the system. 

> 🐥 We only care about students for this feature. When adding the identity to the database, you need to indicate that this record is a student as well.

Technically, a student must provide their identity and the system must persist their identity into the database. The table that we are interested in is `users`. Registration means to insert a new row (containing their identities) into this table.

More importantly, for the security purpose, the system must not store plain password. The password must be hashed using `hash()` function in DuckDB. For example, the following SQL statement will store `12345` as a plaintext.

```sql
INSERT INTO x (y)
VALUES ('12345');
```

If the database gets stolen, the password will be exposed. Since many users tend to reuse their passwords for multiple systems, data thieves could use these passwords to unauthorizedly access other systems.

Instead, the following SQL statement will not store `12345` as a plaintext.

```sql
INSERT INTO x (y)
VALUES (hash('12345'));
```

Instead, it will store only the hash of `12345`, which could be some cryptic strings.

> 🐥 Even though other cryptographic hashing functions are available, for this assignment, you must use the build-in `hash` function in DuckDB.

You must implement function `register` in `models.py`. This function must return a Boolean value indicating whether the identity can be added to the database or not.

### Feature 2 - Authentication (Login)

The system can authenticate each user by matching their identity (i.e., username and password) with the stored identities.

Since we do not store passwords plainly, when you receive a plain password from users, you need to hash it before comparing against the database.

You must implement function `login` in `models.py`. This function must return the user type of the user.

> 🐥 You must check with `views.py` to see appropriate return values for those functions.

## Feature Set 2 - Students

### Feature 3 - Viewing Enrolled Courses

Authenticated students must be able to see all of their enrolled courses.

> 🐥 Students do not have capabilities to enroll in this system. Administrators do.

You must implement function `get_all_courses_by_user` in `models.py`. This function must return a list of `course_id` and `course_name` of courses that a specific user enrolled.

### Feature 4 - Post Pagination

When an authenticated student elects to view posts of a course, the student will see all those posts but only 10 at a time. For example, at first, the student will see the first 10 posts:

```
Post 1
Post 2
...
Post 10
```

The application has an option for the student to go to the next (or previous) set of 10 posts. For example, if the student elects to see the next 10 posts:

```
Post 11
Post 12
...
Post 20
```

If the set contains less then 10 posts, show only them.

First, we recommend you understand `views.py`, especially function `render_course_posts`. You will see how the above functionality was implemented for the user interface. However, for the database side, you still need to implement functions `get_post_count_by_course` and `get_top_ten_course_posts_with_offset` in `models.py` to make this functionality done.

> 🐥 You must check with `views.py` to see appropriate return values for those functions.

### Feature 5 - Creating a Post

An authenticated student must be able to create a post. Each post has its title and its post content.

You must implement function `create_course_post` in `models.py`.

### Feature 6 - Updating/Deleting a Post

An authenticated student must be able to update/delete a post.

You must implement functions `get_post_count_by_author_and_course`, `get_posts_by_author_and_course`, `update_post`, and `delete_post` in `models.py`.

## Feature Set 3 - Administrators

### Feature 7 - Creating a Course

An authenticated administrator must be able to create a course.

You must implement function `create_course` in `models.py`.

### Feature 8 - Student Enrollment

An authenticated administrator must be able to enroll a student to a course.

You must implement function `add_user_to_course` in `models.py`.

### Feature 9 - View Summary

An authenticated administrator must be able to view the summary of the system. Specifically, the summary will tell, for each course:

- How many students in the course?
- How many posts in the course?

You must implement function `get_users_and_post_count_in_course` in `models.py`.

> 🐥 You must consult with function `reader_admin_dashboard` in `views.py` to see appropriate return values.

> 🐥 You must rename columns in the output to match with `views.py`.

## Local Testing

> 🐥 You must not test your code using BigGrade. Use our local testing script. 

You can check whether your implementation is correct by running our test suite. We implement the suite using `pytest`. You can easily run it by installing `pytest` module on your machine as follows:

```
pip install -U pytest
```

Check that you installed correctly:

```
pytest --version
```

Make sure that you are in the outermost directory and use the following command:

```
pytest
```

If you run correctly, you should see something like this:

```
...
FAILED src/tests/unit/test_select.py::test_both_constant_false - AttributeError: 'NoneType' object has no attribute 'rows'
FAILED src/tests/unit/test_select.py::test_type_error_both_identifier - Failed: DID NOT RAISE <class 'TypeError'>
FAILED src/tests/unit/test_select.py::test_type_error_one_identifier - Failed: DID NOT RAISE <class 'TypeError'>
FAILED src/tests/unit/test_select.py::test_type_error_both_constant_float_int - Failed: DID NOT RAISE <class 'TypeError'>
FAILED src/tests/unit/test_select.py::test_type_error_both_constant_int_str - Failed: DID NOT RAISE <class 'TypeError'>
FAILED src/tests/unit/test_select.py::test_multiple_predicates - AttributeError: 'NoneType' object has no attribute 'rows'
======================================================= 36 failed, 8 passed in 0.18s ========================================================
```

Note that this depends on how correct your implementation is.

## Submission

Download your repository as a ZIP file. Go to [BigGrade](https://biggrade.pnx.guide) and upload the ZIP file onto the assignment. Your submission will be autograded. Note that BigGrade only grades the correctness (not the code quality and your understanding).

## Grading Rubric

There are three phases on grading your assignment: Correctness, Code Quality, and Code Understanding.

### Correctness (69%)

Your implementation must pass all of our test cases. You may receive partial scores if your implementation can pass some cases.

Our test cases are broken down into three levels, as follows.

#### Unit Test (39%)

Those test cases exercise whether each method is working correctly or not. Functions under test are all functions in `models.py`.

#### Integration Test (20%)

Those test cases exercise scenarios where multiple functions are working together.

#### End-to-End Test (10%)

Those test cases mimic real-world workloads to test the robustness of your implementation.

### Code Quality (31%)

All code must be well-documented and clean. You should consult with [PEP 8](https://peps.python.org/pep-0008/).

> 🐥 You do not need to apply all suggestions in [PEP 8](https://peps.python.org/pep-0008/). We are less strict than this.

### Code Understanding

Once you have submitted the code and received scores that you satisfy, you may reserve a check-out slot with us. During the check-out, you will be asked several questions to check your understanding. There are three possible results for the check-out:

- **Good (1.0x)** means you can answer all the required questions.
- **Pass (0.5x)** means you can answer some of the required questions.
- **Fail (0.0x)** means you can answer only a few or none of the required questions.

If you receive **Fail**, you may ask to do another check-out or submit a video recording of you answering the missed questions. Note that you can get at most **Pass (0.5x)** if you are in this circumstance.