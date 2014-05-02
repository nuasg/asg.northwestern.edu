from django.contrib import admin
from models import *


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class AnnouncementAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Alert)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Person)
admin.site.register(Position)
admin.site.register(Committee)
admin.site.register(Project)
admin.site.register(Legislation)
admin.site.register(NewsLink)
admin.site.register(Event, EventAdmin)
admin.site.register(Calendar)
admin.site.register(HomepageSlide)
admin.site.register(Page, PageAdmin)
admin.site.register(Resource)
