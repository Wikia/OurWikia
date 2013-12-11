from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    url('', views.frontpage),
    url(r'w/(\w+)/?', views.subwikia),
    url(r'w/(\w+)/(\d+)/?', views.comments)
)
