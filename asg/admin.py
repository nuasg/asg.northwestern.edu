from django.contrib import admin
from image_cropping import ImageCroppingMixin
from models import *


class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class GoogleCalendarAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class PersonAdmin(ImageCroppingMixin, admin.ModelAdmin):
    ordering = ('-positions__on_exec_board', '-positions__senate_leadership', 'last_name')
    list_display = ('full_name', 'main_position')

class ResourceAdmin(admin.ModelAdmin):
    radio_fields = {
        'type': admin.VERTICAL,
        'users': admin.VERTICAL,
    }
    ordering = ('-is_active', '-users', 'type', 'name')
    list_display = ('name', 'type', 'users', 'is_active')

class LegislationAdmin(admin.ModelAdmin):
    radio_fields = {
        'status': admin.VERTICAL,
    }

class HomepageSlideAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('caption', 'order', 'active')
    ordering = ('-active', 'order', 'caption')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'first_committee', 'active')
    ordering = ('-active', 'committees', 'name')

class ApprovedUserAdmin(admin.ModelAdmin):
    list_display = ('netid', 'position')


admin.site.register(Alert)
admin.site.register(News, NewsAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Position)
admin.site.register(Committee)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Legislation, LegislationAdmin)
admin.site.register(NewsLink)
admin.site.register(GoogleCalendar, GoogleCalendarAdmin)
admin.site.register(HomepageSlide, HomepageSlideAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Upload)
admin.site.register(ApprovedUser, ApprovedUserAdmin)
