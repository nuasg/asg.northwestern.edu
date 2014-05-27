from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from models import *
from forms import *
import itertools
import random

def home(request):
    current_time = timezone.now()
    alerts = Alert.objects.filter(start_time__lte=current_time,
                                  end_time__gt=current_time)
    announcements = Announcement.objects.order_by('-date_posted')[:2]
    bills = Legislation.objects.all()[:5]
    news_links = NewsLink.objects.order_by('-date_published')[:5]
    slides = HomepageSlide.objects.filter(active=True)
    calendars = GoogleCalendar.objects.filter(show_on_homepage=True)
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
    calendars = GoogleCalendar.objects.filter(display_on_calendar_page=True)
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

def contact(request):
    exec_board_positions = Position.objects.filter(on_exec_board=True)
    senate_leadership_positions = Position.objects.filter(senate_leadership=True)
    return render_to_response('contact.html', locals())

def cabinet(request):
    exec_members = Person.objects.filter(positions__on_exec_board=True)\
                            .order_by('positions__order')
    return render_to_response('cabinet.html', locals())

def senators(request):
    senators = Person.objects.filter(positions__name='Senator')
    return render_to_response('senators.html', locals())

def projects(request):
    # iterator() doesn't supply count()
    projects = Project.objects.all()
    random.shuffle(list(projects))
    return render_to_response('projects.html', locals())

def view_project(request, id):
    project = get_object_or_404(Project, id=int(id))
    return render_to_response('view_project.html', locals())

def people(request, id):
    'Display the profile of a single person'
    person = get_object_or_404(Person, id=int(id))
    return render_to_response('person.html', locals())

@login_required
def edit_profile(request):
    'A page for the logged-in user to edit his/her own profile'
    person = get_object_or_404(Person, user=request.user)
    if request.method == 'GET':
        person_form = PersonForm(instance=person)
    elif request.method == 'POST':
        # User submitted the form; update fields
        person_form = PersonForm(request.POST, instance=person)
        if person_form.is_valid():
            # Save the updated data
            person_form.save()
            update_success = True
    return render_to_response('edit_profile.html', locals(),
                context_instance=RequestContext(request))
