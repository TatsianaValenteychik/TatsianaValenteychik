class Post:
    def __init__(self, post_id, body, author):
        self.post_id = post_id
        self.body = body
        self.author = author
        self.reactions = []
    