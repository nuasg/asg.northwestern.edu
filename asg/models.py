import tinymce.models as tmodels
from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField


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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True)
    date_joined = models.DateField(blank=True, null=True)
    positions = models.ManyToManyField('Position', blank=True)
    bio = models.TextField(blank=True)
    photo = models.FileField(upload_to='profile_photos', blank=True)

    website_role = models.CharField(max_length=4, choices=WEBSITE_ROLES, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)

    # Person will have projects, committees from
    # fields in those models

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = 'People'
        ordering = ['last_name']


class Position(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # For director positions on committees, etc.
    committee = models.ForeignKey('Committee', null=True, blank=True)

    order = models.IntegerField(blank=True)
    on_exec_board = models.BooleanField(default=True)
    senate_leadership = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['on_exec_board', 'senate_leadership', 'order']

    def __unicode__(self):
        return self.name


class Committee(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField('Person')

    # Some committees might be for the Executive VP's pet projects,
    # for example, and we don't want to show those on the Committee page
    show_in_list = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = tmodels.HTMLField(blank=True)
    committee = models.ForeignKey('Committee')

    primary_contact = models.ForeignKey('Person', null=True, blank=True, related_name='+')
    members = models.ManyToManyField('Person')

    def __unicode__(self):
        return '%s: %s' % (self.committee, self.name)



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
    status = models.CharField(max_length=4, choices=LEGISLATION_STATUSES)
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
    xml_feed_url = models.URLField()
    is_public = models.BooleanField(default=False)
    is_office_hours = models.BooleanField(default=False)
    event_color = ColorField(blank=True)

    def __unicode__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    date = models.DateTimeField()
    location = models.CharField(max_length=455, blank=True)
    description = models.TextField(blank=True)
    calendar = models.ForeignKey('GoogleCalendar', null=True, blank=True)
    
    # Exec board members usually have office hours. Avoiding
    # a separate 'Position' model for simplicity. 
    person = models.ForeignKey('Person', related_name='office_hours', null=True, blank=True)

    # Optional associations
    project = models.ForeignKey('Project', null=True, blank=True)
    committee = models.ForeignKey('Committee', null=True, blank=True)

    def __unicode__(self):
        return '%s at %s' % (self.name, self.list_render())

    def list_render(self):
        location_str = ''
        if self.location:
            location_str = ', ' + self.location
        time = self.date.strftime('%I').lstrip('0')
        ampm = self.date.strftime('%p').lower()
        day = self.date.strftime('%d').lstrip('0')
        return self.date.strftime('{}{}, %a %b {}'.format(time, ampm, day)) + location_str


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
    logo_image = models.FileField(upload_to='resource_logos', blank=True)
    type = models.CharField(max_length=1, choices=RESOURCE_TYPES)
    users = models.CharField(max_length=2, choices=RESOURCE_USERS)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)

    def __unicode__(self):
        return '%s for %s: %s' % (self.get_type_display(),
                                  self.get_users_display(),
                                  self.name)

    class Meta:
        verbose_name_plural = 'Resources and Services'


