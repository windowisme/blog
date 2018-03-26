from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
from pymongo import MongoClient
from Post import Post
from Comment import Comment


app = Flask(__name__)
api = Api(app)
mongo = PyMongo(app)
dbClient = MongoClient('127.0.0.1', 27017)
dbClient.admin.command('ismaster')
db = dbClient.blogDb
postTable = db.post
commentTable = db.comment

class PostApiCommand():
    EDIT = "edit"
    PUBLISH = "publish"
    REMOVE  = "remove"
    DRAFTS  = "drafts"
    COMMENT = "comment"

class CommentApiCommand():
    APPROVE = "approve"
    REMOVE  = "remove"

class PostListApi(Resource):

    def get(self):

        print("PostListApi.get()")
        if PostApiCommand.DRAFTS in request.path:
            draft_list = [ Post(draft).as_dict() for draft in postTable.find({Post.PUBLISHED_DATE : ""}).sort(Post.CREATED_DATE, 1)]
            print(draft_list)
            return { Post.POSTS : draft_list }
        else:
#        print(dir(request))
#        print("base_url: " + request.base_url)
#        print("full_path: " + request.full_path)
#        print("url: " + request.url)
#        print("host_url: " + request.host_url)
#        print("path: " + request.path)
#        print("args: " + str(request.args))
#        print(postTable.find())
            post_list = [ Post(originalPost).as_dict() for originalPost in postTable.find({ Post.PUBLISHED_DATE : { "$ne" : "" } })] 
            print(post_list)
            return { Post.POSTS : post_list }
#        return None

class PostApi(Resource):

    def _update_post(self, post_hash, data):
        print("PostApi._update_post(): " + str(data))
        postTable.update_one({ Post.HASH : post_hash },
                             { "$set" : data })
    
    def get(self, post_hash):
        print("PostApi.get(): %s", post_hash)
        originalPost = postTable.find({ Post.HASH : post_hash })[0]
        post = Post(originalPost).as_dict()
        commend_list = [ Comment(originalComment).as_dict() for originalComment in commentTable.find({ Comment.POST_HASH : post[Post.HASH] })]
        post[Comment.COMMENTS] = commend_list
        print(post)
        return post


    def put(self, post_hash, command):
        print("PostApi.put(): %s %s" % (command, post_hash))
        
        if command == PostApiCommand.EDIT:
            post = request.json
            self._update_post(post_hash, post)
        elif command == PostApiCommand.PUBLISH:
            published_date = request.json 
            self._update_post(post_hash, published_date)

    def post(self):
        print("PostApi.post(): got a post_new request")
        aPost = request.json
        id = postTable.insert_one(aPost[Post.POST]) 
        post_hash = hash(str(id.inserted_id))
        print("post's hash: %s" % post_hash)
        postTable.update_one({ Post.ID : id.inserted_id }, 
                             { "$set": { Post.HASH : str(post_hash) }})
        print(aPost)
        return post_hash
    
    def delete(self, post_hash):
        print("PostApi.delete(): got a delete request: %s" % post_hash)
        commentTable.delete_many({ Comment.POST_HASH : post_hash })
        result = postTable.delete_one({ Post.HASH : post_hash })
        print(result.deleted_count)

class CommentApi(Resource):
  
    def _get_post_hash(self, comment_hash):
        originalComment = commentTable.find({ Comment.HASH : comment_hash })[0]
        comment = Comment(originalComment).as_dict()
        return comment[Comment.POST_HASH]

    def get(self, comment_hash):
        print("CommentApi.get(): got a get_comment request.")
        return { Comment.POST_HASH : self._get_post_hash(comment_hash) }
 
    def put(self, comment_hash):
        print("CommentApi.put(): got a comment_approve request.")
        commentTable.update_one({ Comment.HASH : comment_hash },
                                { "$set" : { Comment.IS_APPROVED : True }})
        post_hash = self._get_post_hash(comment_hash)
        comment_count = Post(postTable.find({ Post.HASH : post_hash})[0]).as_dict()[Post.COMMENT_COUNT]
        comment_count += 1
        postTable.update({ Post.HASH : post_hash }, 
                         { "$set" : { Post.COMMENT_COUNT : comment_count } })
#        postTable.update_one({ Post.HASH : self._get_post_hash(comment_hash) },
#                             { "$inc" : { Post.COMMENT_COUNT, 1 }})
    def post(self, post_hash):
        print("CommentApi.post(): got a add_comment request")
        aComment= request.json
        id = commentTable.insert_one(aComment[Comment.COMMENT]) 
        comment_hash = hash(str(id.inserted_id))
        print("comment's hash: %s" % comment_hash)
        commentTable.update_one({ Comment.ID : id.inserted_id}, 
                                { "$set": { Comment.HASH : str(comment_hash) }})
        print(aComment)
        return comment_hash
    
    def delete(self, comment_hash):

        print("CommentApi.delete(): got a delete comment request: %s" % comment_hash)
        result = commentTable.delete_one({ Comment.HASH : comment_hash })
        print(result.deleted_count)


api.add_resource(PostListApi, '/', '/drafts/')
api.add_resource(PostApi, 
                '/post/<string:post_hash>/', 
                '/post/new/',
                '/post/<string:command>/<string:post_hash>/',
                '/post/remove/<string:post_hash>/')

api.add_resource(CommentApi,
                '/comment/<string:comment_hash>/', 
                '/post/<string:post_hash>/comment/',
                '/comment/approve/<string:comment_hash>/',
                '/comment/delete/<string:comment_hash>/')

if __name__ == '__main__':
    app.run(debug=True)
       
