from django.conf.urls import patterns, url
import views
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
                       url(r'w/(\w+)/?', views.subwikia),
                       url(r'w/([^/]+)/(\d+)/?', views.comments),
                       url(r'(\d+)/upvote/?', views.upvote),
                       url(r'(\d+)/downvote/?', views.downvote),
                       url(r'^accounts/profile/?$', RedirectView.as_view(url='/', permanent=False)),
                       url(r'', views.frontpage))
