from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'w/(\w+)/?', views.subwikia),
                       url(r'w/([^/]+)/(\d+)/?', views.comments),
                       url(r'w/(\d+)/upvote', views.upvote),
                       url(r'w/(\d+)/downvote', views.downvote),
                       url(r'', views.frontpage))
