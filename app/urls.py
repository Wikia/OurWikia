from django.conf.urls import patterns, include, url
import views
from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^admin/?', include(admin.site.urls)),
                       url(r'w/([^/]+)/(\d+)/?', views.comments),
                       url(r'w/(\w+)/?', views.subwikia),
                       url(r'(\d+)/upvote/?', views.upvote),
                       url(r'(\d+)/downvote/?', views.downvote),
                       url(r'^accounts/profile/?$', RedirectView.as_view(url='/', permanent=False)),
                       url(r'', views.frontpage))
