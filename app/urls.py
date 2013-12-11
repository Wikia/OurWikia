from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
                       url(r'w/(\w+)/?', views.subwikia),
                       url(r'w/([^/]+)/(\d+)/?', views.comments),
                       url(r'', views.frontpage))

