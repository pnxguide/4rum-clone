import sys
import models

from utils import display_edit_post, display_posts, display_title

def render_unauthenticated():
    while True:
        display_title("Current Screen: Unauthenticated")
        print("Please select one of the following options:")
        print(" |- [L]ogin")
        print(" |- [R]egister")
        print(" |- [C]lose")

        command = input("Your Option: ")
        if command == "L":
            username = input("Username: ")
            password = input("Password: ")
            user_type = models.login(username, password)
            if user_type == "STUDENT":
                render_courses(username)
            elif user_type == "ADMIN":
                render_admin_panel()
            else:
                print()
                print("Authentication failed. Please try again.")
        elif command == "R":
            username = input("Username: ")
            password = input("Password: ")
            if models.register(username, password):
                print()
                print("Registration succeed!")
            else:
                print()
                print("Registration failed. Please try again.")
        elif command == "C":
            break
        else:
            print()
            print("Wrong command. Please try again.")
        
        print()

def render_courses(username: str):
    courses = models.get_all_courses_by_user(username)

    while True:
        display_title("Current Screen: Course Selection")
        print("Please select one of the following options:")
        for course in courses:
            print(f" |- [{course['course_id']}] {course['course_name']}")
        print(" |- [L]ogout")

        command = input("Your Option: ")
        if command == "L":
            break
        else:
            is_command_valid = False

            # Search for the course in the `courses` list
            # If found, proceed to render posts in the course
            for course in courses:
                if command == course["course_id"]:
                    render_course_posts(command, username)
                    is_command_valid = True
                    break
            
            if not is_command_valid:
                print()
                print("Wrong command. Please try again.")
        
        print()

def render_modify_course_posts(course_id: int, username: str):
    current_offset = 0

    while True:
        post_count = models.get_post_count_by_author_and_course(username, course_id)
        if post_count == 0:
            print("No posts to edit.")
            return
        
        display_title("Current Screen: Edit Course Posts")
        print()

        posts = models.get_posts_by_author_and_course(username, course_id, current_offset)
        display_edit_post(posts)
        print()
        print("Please select one of the following options:")
        if current_offset != 0:
            print(" |- [P]revious ten posts")
        if current_offset + 10 < post_count:
            print(" |- [N]ext ten posts")
        print(" |- [E]dit a post")
        print(" |- [D]elete a post")
        print(" |- [L]eave Editing")

        command = input("Your Option: ")
        if current_offset != 0 and command == "P":
            current_offset -= 10
        elif current_offset + 10 < post_count and command == "N":
            current_offset += 10
        elif command == "L":
            break
        elif command == "E":
            post_id = int(input("Post ID "))
            title = input("New Post Title: ")
            content = input("New Post Content: ")
            if models.update_post(post_id, title, content):
                print()
                print("Post update succeed. Please try again.")
            else:
                print()
                print("Post update failed. Please try again.")
        elif command == "D":
            post_id = int(input("Post ID "))
            if models.delete_post(post_id):
                print()
                print("Post deletion succeed. Please try again.")
            else:
                print()
                print("Post deletion failed. Please try again.")
        else:
            print("Wrong command. Please try again.")
        
        print()

def render_course_posts(course_id: int, username: str):
    current_offset = 0

    post_count = models.get_post_count_by_course(course_id)

    while True:
        display_title("Current Screen: Course Posts")
        print()
        posts = models.get_top_ten_course_posts_with_offset(course_id, current_offset)
        display_posts(posts)
        print()
        print("Please select one of the following options:")
        if current_offset != 0:
            print(" |- [P]revious ten posts")
        if current_offset + 10 < post_count:
            print(" |- [N]ext ten posts")
        print(" |- [C]reate a new post")
        print(" |- [M]odify posts")
        print(" |- [L]ogout")

        command = input("Your Option: ")
        if current_offset != 0 and command == "P":
            current_offset -= 10
        elif current_offset + 10 < post_count and command == "N":
            current_offset += 10
        elif command == "C":
            title = input("Post Title: ")
            content = input("Post Content: ")
            if models.create_course_post(course_id, title, content, username):
                print()
                print("Post creation succeed. Please try again.")
            else:
                print()
                print("Post creation failed. Please try again.")
        elif command == "M":
            render_modify_course_posts(course_id, username)
            post_count = models.get_post_count_by_course(course_id)
        elif command == "L":
            break
        else:
            print("Wrong command. Please try again.")
        
        print()

def reader_admin_dashboard():
    display_title("Current Screen: Admin Dashboard Summary")
    print()

    user_cnt_in_courses = models.get_users_and_post_count_in_course()
    print("+"+f"{'-'*51}" + "+" + f"{'-'*16}" + "+" + f"{'-'*16}" + "+")
    print(f"| " + "Course Name".ljust(50) + "| " + "User Count".ljust(15) + "| " + "Post Count".ljust(15) + "|")
    print("+"+f"{'-'*51}" + "+" + f"{'-'*16}" + "+" + f"{'-'*16}" + "+")
    for data in user_cnt_in_courses:
        print("| " + f"{data['course_name']}".ljust(50) + "| " + f"{data['user_count']}".ljust(15) + "| " + f"{data['post_count']}".ljust(15) + "|")
    print("+"+f"{'-'*51}" + "+" + f"{'-'*16}" + "+" + f"{'-'*16}" + "+")
    print()
    
def render_admin_panel():
    while True:
        display_title("Current Screen: Admin Panel")
        print("Please select one of the following options:")
        print(" |- Create a new [C]ourse")
        print(" |- [D]ashboard")
        print(" |- [A]dd a user to a course")
        print(" |- [L]ogout")

        command = input("Your Option: ")
        if command == "C":
            course_name = input("Course Name: ")
            if models.create_course(course_name):
                print()
                print("Course creation succeed. Please try again.")
            else:
                print()
                print("Course creation failed. Please try again.")
        elif command == "A":
            username = input("Username: ")
            course_id = input("Course ID: ")
            if models.add_user_to_course(username, course_id):
                print()
                print("Add user succeed. Please try again.")
            else:
                print()
                print("Add user failed. Please try again.")
        elif command == "D":
            reader_admin_dashboard()
        elif command == "L":
            break
        else:
            print("Wrong command. Please try again.")
        
        print()
