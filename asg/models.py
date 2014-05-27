import urllib
import urlparse
import tinymce.models as tmodels
from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from image_cropping import ImageRatioField, ImageCropField


class Alert(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    message = tmodels.HTMLField()

    def __unicode__(self):
        return '%s: %s' % (self.start_time, self.message)


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    link_title_to = models.URLField(blank=True)
    slug = models.SlugField()
    message = tmodels.HTMLField()

    date_posted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s: %s' % (self.date_posted.date(), self.title)


# Will be used for editing permissions on the website
WEBSITE_ROLES = [
    ('EXEC', 'Executive Board Officer'),
    ('CMEM', 'Committee Member'),
    ('SEN', 'Senator')
]
class Person(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    netid = models.CharField(max_length=6, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True)
    date_joined = models.DateField(blank=True, null=True, help_text='The date you first joined ASG')
    positions = models.ManyToManyField('Position', blank=True)
    bio = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    photo = ImageCropField(upload_to='profile_photos', blank=True, null=True, default='settings.MEDIA_ROOT/profile_photos/default.jpg')
    thumbnail_size = ImageRatioField('photo', '200x200', size_warning=True)

    website_role = models.CharField(max_length=4, choices=WEBSITE_ROLES, blank=True)

    # Person will have projects, committees from
    # fields in those models

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = 'People'
        ordering = ['last_name', 'first_name']


class Position(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True, help_text='The official @u email for this position, if it has one')
    description = models.TextField(blank=True, null=True)
    
    # For director positions on committees, etc.
    committee = models.ForeignKey('Committee', null=True, blank=True, help_text='The committee that the person in this position oversees')

    order = models.IntegerField(blank=True, null=True)
    on_exec_board = models.BooleanField(default=True)
    senate_leadership = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['on_exec_board', 'senate_leadership', 'order']

    def __unicode__(self):
        return self.name


class Committee(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField('Person', blank=True, null=True)

    # Some committees might be for the Executive VP's pet projects,
    # for example, and we don't want to show those on the Committee page
    show_in_list = models.BooleanField(default=True, help_text='Uncheck this for committees that shouldn\'t appear on the Committees page')

    def __unicode__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    short_desc = models.TextField(blank=True)
    description = tmodels.HTMLField(blank=True)
    committees = models.ManyToManyField('Committee', blank=True, null=True)

    primary_contact = models.ForeignKey('Person', null=True, blank=True, related_name='+')
    members = models.ManyToManyField('Person', blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s: %s' % (self.committees.first(), self.name)



LEGISLATION_STATUSES = [
    ('WD', 'Withdrawn'),
    ('SU', 'Submitted'),
    ('PV', 'Pending vote'),
    ('PA', 'Passed'),
    ('DF', 'Defeated')
]
class Legislation(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=2, choices=LEGISLATION_STATUSES, blank=True)
    status_date = models.DateField(blank=True)
    link = models.URLField(blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.code, self.name)

    class Meta:
        ordering = ['-status_date', '-code']

    

NEWS_SOURCES = [
    ('NBN', 'North by Northwestern'),
    ('DLY', 'The Daily Northwestern'),
]
class NewsLink(models.Model):
    source = models.CharField(max_length=3, choices=NEWS_SOURCES)
    name = models.CharField(max_length=140)
    link = models.URLField()
    date_published = models.DateField()

    def __unicode__(self):
        return '%s: %s via %s' % (self.date_published, self.name, self.get_source_display())

    class Meta:
        verbose_name_plural = 'News Links'
        ordering = ['-date_published']


# Events from these calendars are shown on the Events page
# unless is_public is False
class GoogleCalendar(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    xml_feed_url = models.URLField()
    calendar_id = models.TextField(editable=False)
    display_on_calendar_page = models.BooleanField(default=True)
    display_by_default = models.BooleanField(default=True)
    show_on_homepage = models.BooleanField(default=False)
    is_office_hours = models.BooleanField(default=False)
    event_color = ColorField(blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Extract Google Calendar ID from XML feed URL
        path = urlparse.urlparse(urllib.unquote(self.xml_feed_url)).path
        self.calendar_id = path.split('/')[3]
        super(GoogleCalendar, self).save(*args, **kwargs)

class HomepageSlide(models.Model):
    image = models.ImageField(upload_to='homepage_slides')
    link = models.URLField(blank=True)
    caption = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    order = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.caption

    class Meta:
        verbose_name_plural = 'Homepage slides'
        ordering = ['active', 'order', 'caption']

PAGE_WIDTHS = (
    ('9', 'Default'),
    ('12', 'Full'),
)
class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    width = models.CharField(max_length=2, choices=PAGE_WIDTHS, default='9')
    content = tmodels.HTMLField()

    def __unicode__(self):
        return self.title


RESOURCE_TYPES = (
    ('R', 'Resource'),
    ('S', 'Service'),
)
RESOURCE_USERS = (
    ('ST', 'Students'),
    ('SG', 'Student Groups'),
)
class Resource(models.Model):
    name = models.CharField(max_length=100, blank=True)
    logo_image = models.ImageField(upload_to='resource_logos', blank=True, help_text='If you provide a logo, it will be displayed instead of the name')
    type = models.CharField(max_length=1, choices=RESOURCE_TYPES)
    users = models.CharField(max_length=2, choices=RESOURCE_USERS)
    description = models.TextField(blank=True)
    page = models.ForeignKey('Page', null=True, blank=True)
    link = models.URLField(blank=True, help_text='If you enter a link, it will be used instead of the resource being linked to the website page')

    def __unicode__(self):
        return '%s for %s: %s' % (self.get_type_display(),
                                  self.get_users_display(),
                                  self.name)

    class Meta:
        verbose_name_plural = 'Resources and Services'


class Upload(models.Model):
    file = models.FileField(upload_to='uploads')

    def __unicode__(self):
        return unicode(self.file)


class ApprovedUser(models.Model):
    netid = models.CharField(max_length=6)
    position = models.ForeignKey('Position')

    def __unicode__(self):
        return unicode(self.netid)
