import json
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect 
from django.utils import timezone
from .forms import PostForm, CommentForm
from .models import Post as DjPost 
from .models import Comment as DjComment
from blog.flaskApi.Post import Post
from blog.flaskApi.Comment import Comment
from . import requester
from django.urls import reverse
from django.views.decorators.cache import never_cache    

def post_list(request):
    posts = requester.get_post_list()
    return render(request, 'blog/post_list.html', {"posts" : posts})

@never_cache
def post_detail(request, post_hash):
    print("views.post_detail()")
    print(post_hash)
    post = requester.get_post_detail(post_hash)
    print(post)
    return render(request, 'blog/post_detail.html', {"post" : post})

@login_required
def post_new(request):
    print("post_new()")
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            pfPost = form.save(commit=False)
            post = Post.init_fromForm(pfPost, request.user.get_username())
            post_hash = requester.post_new({Post.POST:post.as_dict()})
            return redirect('post_detail', post_hash=post_hash)
    else:
        form = PostForm()
    print("post_new(): form object - " + str(form))
    return render(request, 'blog/post_edit.html', {'form' : form})

@login_required
def post_edit(request, post_hash):
    print("views.post_edit(): %s" % post_hash)
    post = requester.get_post_detail(post_hash)
    djPost = DjPost( title = post[Post.TITLE],
                     text  = post[Post.CONTENT])
    if request.method == 'POST':
        print("go rendering detail page.")
        form = PostForm(request.POST, instance=djPost)
        if form.is_valid():
            pfPost = form.save(commit=False)
            post[Post.TITLE]   = pfPost.title
            post[Post.CONTENT] = pfPost.text
            requester.edit_post({Post.POST : post}, post[Post.HASH])
            return redirect('post_detail', post_hash = post[Post.HASH])
    else:
        print("go rendering edit page.")
        form = PostForm(instance=djPost)
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
@never_cache
def post_draft_list(request):
    posts = requester.get_drafts_list()
    print("views.post_draft_list(): " + str(posts))
    return render(request, 
                  'blog/post_draft_list.html',
                  {'posts' : posts})

@login_required
def post_publish(request, post_hash):
    requester.publish_post(post_hash)
    return redirect('post_detail', post_hash=post_hash)

@login_required
def post_remove(request, post_hash):
    requester.remove_post(post_hash)
    return redirect('post_list')

@never_cache
def add_comment_to_post(request, post_hash):
    print("views.add_comment_to_post(): %s" % post_hash)  
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            djComment = form.save(commit=False)
            comment = Comment.init_fromForm(djComment, 
                                            request.user.get_username(),
                                            post_hash)
            print(comment)
            requester.add_comment({Comment.COMMENT : comment.as_dict()},
                                   post_hash)
            print("add_comment(): " + str(comment.as_dict()))
            return redirect('post_detail', post_hash=post_hash)
    else:
        form = CommentForm()

    return render(request, 
                  'blog/add_comment_to_post.html',
                  {'form' : form})

@login_required
def comment_approve(request, comment_hash):
    print("views.comment_approve(): %s" % comment_hash)
    post_hash = requester.get_comment_post_hash(comment_hash)
    requester.approve_comment(comment_hash)
    return redirect('post_detail', post_hash=post_hash)

@login_required
def comment_remove(request, comment_hash):
    print("views.comment_remove(): %s" % comment_hash)
    post_hash = requester.get_comment_post_hash(comment_hash)
    requester.delete_comment(comment_hash)
    return redirect('post_detail', post_hash=post_hash)
