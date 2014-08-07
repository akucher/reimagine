from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reimagine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^profile', 'reimagine.views.profile', name='profile'),
    url(r'^admin/', include(admin.site.urls)),
)
