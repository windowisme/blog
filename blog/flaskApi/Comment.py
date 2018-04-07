

class Comment:
    
    ID           = "_id"
    COMMENT      = "comment"
    COMMENTS     = "comments"
    AUTHOR       = "author"
    CONTENT      = "content"
    CREATED_DATE = "created_date"
    IS_APPROVED  = "is_approved"
    HASH         = "hash"
    POST_HASH    = "post_hash"

    def __init__(self, data):
        print("init Comment object")
        print(data)
        
        self.author       = data[self.AUTHOR]
        self.content      = data[self.CONTENT]
        self.created_date = data[self.CREATED_DATE]
        self.is_approved  = data[self.IS_APPROVED]
        self.hash         = (data[self.HASH] if self.HASH in data.keys() else "")
        self.post_hash    = data[self.POST_HASH]

    @classmethod
    def init_fromForm(cls, commentForm, username, post_hash):
        print("init Comment object from CommentForm")
        return cls({cls.AUTHOR         : username,
                    cls.CONTENT        : commentForm.text,
                    cls.CREATED_DATE   : str(commentForm.created_date.now()),
                    cls.IS_APPROVED    : False,
                    cls.HASH           : "",
                    cls.POST_HASH      : post_hash})


    def as_dict(self):
        return {self.AUTHOR       : self.author,
                self.CONTENT      : self.content,
                self.CREATED_DATE : self.created_date,
                self.IS_APPROVED  : self.is_approved,
                self.HASH         : self.hash,
                self.POST_HASH    : self.post_hash}
        
