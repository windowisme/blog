import json
import sys
import requests
from datetime import datetime
from blog.flaskApi.Post import Post
from blog.flaskApi.Comment import Comment
from blog.predata import api_post_new
from blog.predata import api_post_modified
from blog.predata import api_comment_new

SERVICE_URL = "http://127.0.0.1:5000/"

def post_new(post):
    print("request post_new(): " + json.dumps(post))
    r = requests.post(SERVICE_URL + 'post/new/', json = post)
    print("url: %s, %s" % (r.url, r.text))
    return r.text.rstrip('\n')

def edit_post(post = None, post_hash = ""):
    print("request edit_post(): %s" % str(post))
    r = requests.put(SERVICE_URL + "post/edit/" + post_hash + "/",
                      json = post[Post.POST])
    print("url: %s, %s" % (r.url, r.text))

def publish_post(post_hash):
    print("request publish_post: " + SERVICE_URL + ("post/publish/%s/" % post_hash))
    r = requests.put(SERVICE_URL + ("post/publish/%s/" % post_hash), 
                     json = {Post.PUBLISHED_DATE : str(datetime.now())})

def get_post_list():
    print("request get_post_list")
    r = requests.get(SERVICE_URL)
    post_list = r.json()
    print("posts gotten are: " + str(post_list[Post.POSTS]))    
    return post_list[Post.POSTS]

def get_drafts_list():
    print("request get drafts")
    r = requests.get(SERVICE_URL + "drafts/")
    drafts_list = r.json()
    print("drafts gotten are: " + str(drafts_list[Post.POSTS]))
    return drafts_list[Post.POSTS]

def get_post_detail(post_hash):
    print("request post_detail: " + str(post_hash))
    r = requests.get(SERVICE_URL + ("post/%s/" % post_hash))
    aPost = r.json()
    print("data gotten is: " + str(aPost))
    return aPost

def remove_post(post_hash):
    print("request remove: " + SERVICE_URL + ("post/remove/%s/" % post_hash))
    r = requests.delete(SERVICE_URL + ("post/remove/%s/" % post_hash))

def get_comment_post_hash(comment_hash):
    print("get_comment(): %s" % comment_hash)
    r = requests.get(SERVICE_URL + ("comment/%s/" % comment_hash))
    aComment = r.json()
    return aComment[Comment.POST_HASH]


def add_comment(comment = None, post_hash = ""):
    comment[Comment.COMMENT][Comment.POST_HASH] = post_hash        
    print("add_comment(): " + json.dumps(comment))
    r = requests.post(SERVICE_URL + ("post/%s/comment/" % post_hash), json = comment)
    print("url: %s, %s" % (r.url, r.text))

def approve_comment(comment_hash):
    print("approve_comment(): %s" % comment_hash)
    r = requests.put(SERVICE_URL + 'comment/approve/%s/' % comment_hash)
    print("url: %s, %s" % (r.url, r.text))

def delete_comment(comment_hash):
    print("request delete comment: " + SERVICE_URL + ("comment/delete/%s/" % comment_hash))
    r = requests.delete(SERVICE_URL + ("comment/delete/%s/" % comment_hash))

if __name__ == '__main__':
    from flaskApi.Post import Post
    from flaskApi.Comment import Comment
    from predata import api_post_new
    from predata import api_post_modified
    from predata import api_comment_new
    
    print(sys.argv[1])
    if sys.argv[1] == 'post_new':
        post_new("none")
    elif sys.argv[1] == 'get_post_list':
        get_post_list()
    elif sys.argv[1] == 'get_drafts_list':
        get_drafts_list()
    elif sys.argv[1] == 'get_post_detail':
        get_post_detail(sys.argv[2])
    elif sys.argv[1] == 'remove_post':
        print(sys.argv[2])
        remove_post(sys.argv[2])
    elif sys.argv[1] == "publish":
        publish_post(sys.argv[2])
    elif sys.argv[1] == "edit":
        edit_post(post_hash = sys.argv[2])
    elif sys.argv[1] == "add_comment":
        add_comment(post_hash=sys.argv[2])
    elif sys.argv[1] == "approve_comment":
        approve_comment(sys.argv[2])
    elif sys.argv[1] == "delete_comment":
        delete_comment(sys.argv[2])
