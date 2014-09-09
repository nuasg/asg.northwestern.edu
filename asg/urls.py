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
    url(r'^office-hours/', 'office_hours'),
    url(r'^calendar/', 'calendar'),
    url(r'^news/$', 'list_news'),
    url(r'^news/(?P<year>\d+)/(?P<month>\d+)/(?P<slug>[\w-]+)/$', 'news'),
    url(r'^legislation/$', 'list_legislation'),
    url(r'^in-the-news/$', 'list_news_links'),
    url(r'^contact/', 'contact'),
    url(r'^cabinet/', 'cabinet'),
    url(r'^senators/', 'senators'),
    url(r'^projects/(?P<id>\d+)/([\w-]+/)?$', 'view_project'),
    url(r'^projects/', 'projects'),
    url(r'^committees/', 'committees'),
    url(r'^people/(?P<id>\d+)/([\w-]+/)?$', 'people'),
    url(r'^edit_profile/', 'edit_profile'),
    url(r'^login/', 'login_user'),
    url(r'^blog/', 'blog'),
    url(r'^tools/', 'exec_tools'),
    url(r'^export_roster/', 'export_roster'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('', 
    url(r'^logout/', 'django.contrib.auth.views.logout', 
            {'next_page': '/'}),

    # Pages with root slugs must go last
    url(r'^(?P<page_slug>[\w-]+)/$', 'asg.views.page'),
)
