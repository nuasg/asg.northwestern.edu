import datetime
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import *

def home(request):
    current_time = datetime.datetime.now()
    alerts = Alert.objects.filter(start_time__lte=current_time,
                                  end_time__gt=current_time)
    print Alert.objects.all()
    print alerts
    announcements = Announcement.objects.order_by('-date_posted')[:2]
    bills = Legislation.objects.all()[:5]
    news_links = NewsLink.objects.order_by('-date_published')[:5]
    slides = HomepageSlide.objects.filter(active=True)
    calendars = GoogleCalendar.objects.filter(is_public=True, is_office_hours=False)
    return render_to_response('home.html', locals(),
                context_instance=RequestContext(request))

def page(request, page_slug):
    page = get_object_or_404(Page, slug=page_slug)
    return render_to_response('page.html', locals())

def for_students(request):
    users = 'Student'
    desc = "ASG has all the info you need to know about what's happening every week, how to work with a faculty member, how to propose a new project, and more. Our online services help you find a job, sell/buy your books, and get a cab, while our fairs provide opportunities to connect with student groups and find off-campus housing."
    resources = Resource.objects.filter(type='R', users='ST')
    services = Resource.objects.filter(type='S', users='ST')
    return render_to_response('resources.html', locals(),
                context_instance=RequestContext(request))

def for_groups(request):
    users = 'Student Group'
    desc = 'Want to know how to start a new student group, finance it, or publicize it? Check out our 2013-14 Student Handbook for all this and more. Also be sure to read the PR Guide for info on how to flyer, reserve rooms and tables, advertise, and print.'
    resources = Resource.objects.filter(type='R', users='SG')
    services = Resource.objects.filter(type='S', users='SG')
    return render_to_response('resources.html', locals(), 
                context_instance=RequestContext(request))

def calendar(request):
    page_name = 'Calendar'
    calendars = GoogleCalendar.objects.filter(is_public=True)
    return render_to_response('calendar.html', locals())

def office_hours(request):
    page_name = 'Office Hours'
    calendars = GoogleCalendar.objects.filter(is_office_hours=True)
    return render_to_response('calendar.html', locals())

announcements_per_page = 10
def list_announcements(request):
    all_announcements = Announcement.objects.order_by('-date_posted')
    p = Paginator(all_announcements, announcements_per_page)
    last_page = p.num_pages
    pages = xrange(1, last_page+1)
    page = int(request.GET.get('page', 1))
    announcements = p.page(page).object_list
    return render_to_response('list_announcements.html', locals())

legislation_per_page = 10
def list_legislation(request):
    all_legislation = Legislation.objects.order_by('-code')
    p = Paginator(all_legislation, legislation_per_page)
    last_page = p.num_pages
    pages = xrange(1, last_page+1)
    page = int(request.GET.get('page', 1))
    bills = p.page(page).object_list
    return render_to_response('list_legislation.html', locals())

news_links_per_page = 10
def list_news_links(request):
    all_news_links = NewsLink.objects.order_by('-date_published')
    p = Paginator(all_news_links, news_links_per_page)
    last_page = p.num_pages
    pages = xrange(1, last_page+1)
    page = int(request.GET.get('page', 1))
    news_links = p.page(page).object_list
    return render_to_response('list_news_links.html', locals())

def announcement(request, slug):
    from_homepage = 'from_homepage' in request.GET
    announcement = get_object_or_404(Announcement, slug=slug)
    return render_to_response('announcement.html', locals())

