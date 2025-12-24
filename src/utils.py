def display_title(title: str):
    title_len = len(title)
    fancy_title = "+" + ("-" * (title_len + 2)) + "+\n" + \
        "| " + title + " |\n" + \
        "+" + ("-" * (title_len + 2)) + "+"
    print(fancy_title)

def display_posts(posts: list):
    for post in posts:
        title = f"Title: {post['title']}"
        content = f"Content: {post['content']}"
        width = max(len(title), len(content))
        fancy_post = "+" + ("-" * (width + 2)) + "+\n" + \
        "| " + title.ljust(width) + " |\n" + \
        "| " + content.ljust(width) + " |\n" \
        "+" + ("-" * (width + 2)) + "+"

        print(fancy_post)

def display_edit_post(posts: list):
    for post in posts:
        id = f"Post ID: {post['post_id']}"
        title = f"Title: {post['title']}"
        content = f"Content: {post['content']}"
        width = max(len(title), len(content))
        fancy_post = "+" + ("-" * (width + 2)) + "+\n" + \
        "| " + id.ljust(width) + " |\n" + \
        "| " + title.ljust(width) + " |\n" + \
        "| " + content.ljust(width) + " |\n" \
        "+" + ("-" * (width + 2)) + "+"     

        print(fancy_post)