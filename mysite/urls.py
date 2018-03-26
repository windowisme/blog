from django.contrib import admin
from django.contrib.auth import views
from django.conf.urls import include, url

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout', kwargs={'next_page' : '/'}),
#    url(r'^accounts/', include('registration.urls')),
    url(r'', include('blog.urls')),
]
