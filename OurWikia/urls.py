from django.conf.urls import patterns, include, url
from app import urls as app_urls
from registration import auth_urls
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OurWikia.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include(auth_urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
)
