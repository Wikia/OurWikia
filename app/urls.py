from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'w/(\w+)/?', views.subwikia),
                       url(r'w/([^/]+)/(\d+)/?', views.comments),
                       url(r'(\d+)/upvote/?', views.upvote),
                       url(r'(\d+)/downvote/?', views.downvote),
                       url(r'', views.frontpage))
