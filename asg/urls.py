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
    url(r'^announcements/$', 'list_announcements'),
    url(r'^announcements/(?P<slug>[\w-]+)/$', 'announcement'),
    url(r'^legislation/$', 'list_legislation'),
    url(r'^in-the-news/$', 'list_articles'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<page_slug>[\w-]+)/$', 'page'),
)
