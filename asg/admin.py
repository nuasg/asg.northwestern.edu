from django.contrib import admin
from models import *


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class AnnouncementAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class PersonAdmin(admin.ModelAdmin):
    radio_fields = {
        'website_role': admin.VERTICAL,
    }
    list_display = ('full_name', 'website_role')

class ResourceAdmin(admin.ModelAdmin):
    radio_fields = {
        'type': admin.VERTICAL,
        'users': admin.VERTICAL,
    }

class HomepageSlideAdmin(admin.ModelAdmin):
    list_display = ('caption', 'order', 'active')


admin.site.register(Alert)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Position)
admin.site.register(Committee)
admin.site.register(Project)
admin.site.register(Legislation)
admin.site.register(NewsLink)
admin.site.register(Event, EventAdmin)
admin.site.register(Calendar)
admin.site.register(HomepageSlide, HomepageSlideAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Resource, ResourceAdmin)
