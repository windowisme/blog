

class Post:

    ID             = "_id"
    POST           = "post"
    POSTS          = "posts"
    AUTHOR         = "author"
    TITLE          = "title"
    CONTENT        = "content"
    CREATED_DATE   = "created_date"
    PUBLISHED_DATE = "published_date"
    HASH           = "hash"
    COMMENT_COUNT  = "comment_count"
    
    def __init__(self, data):
        print("init Post object")
        print(data)
 
        self.author         = data[self.AUTHOR]
        self.title          = data[self.TITLE]
        self.content        = data[self.CONTENT]
        self.created_date   = data[self.CREATED_DATE]
        self.published_date = data[self.PUBLISHED_DATE]
        self.hash           = (data[self.HASH] if self.HASH in data.keys() else "")
        self.comment_count  = (data[self.COMMENT_COUNT] if self.COMMENT_COUNT in data.keys() else int())

    def as_dict(self):
        return { self.AUTHOR         : self.author,
                 self.TITLE          : self.title,
                 self.CONTENT        : self.content,
                 self.CREATED_DATE   : self.created_date,
                 self.PUBLISHED_DATE : self.published_date,
                 self.HASH           : self.hash,
                 self.COMMENT_COUNT  : self.comment_count }

    @classmethod
    def init_fromForm(cls, postForm, username):
        print("init Post object from PostForm")
        return cls({ cls.AUTHOR         : username,
                     cls.TITLE          : postForm.title,
                     cls.CONTENT        : postForm.text,
                     cls.CREATED_DATE   : str(postForm.created_date.now()),
                     cls.PUBLISHED_DATE : "",
                     cls.HASH           : "",
                     cls.COMMENT_COUNT  : int() })

