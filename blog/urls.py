# blog/urls.py

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',                                   views.post_list,       name='post_list'),
    url(r'^post/(?P<post_hash>-?\d*)/$',         views.post_detail,     name='post_detail'),
    url(r'^post/new/$',                          views.post_new,        name='post_new'),
    url(r'^post/edit/(?P<post_hash>-?\d*)/$',    views.post_edit,       name='post_edit'),
    url(r'^drafts/$',                            views.post_draft_list, name='post_draft_list'),
    url(r'^post/publish/(?P<post_hash>-?\d*)/$', views.post_publish,    name='post_publish'),
    url(r'^post/remove/(?P<post_hash>-?\d*)/$',  views.post_remove,     name='post_remove'),
    url(r'^post/(?P<post_hash>-?\d*)/comment/$', views.add_comment_to_post,   name='add_comment_to_post'),
    url(r'^comment/approve/(?P<comment_hash>-?\d*)/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/remove/(?P<comment_hash>-?\d*)/$',  views.comment_remove,  name='comment_remove'),
    
]
