from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('asg.views',
    # Examples:
    # url(r'^$', 'asg.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'home', name='home'),
    url(r'^for-students/', 'for_students'),
    url(r'^for-groups/', 'for_groups'),
    url(r'^calendar/', 'calendar'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<page_slug>\w+)/$', 'page'),
)
