import datetime
import itertools
import os
import random
import requests
import StringIO
import time
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.core.paginator import Paginator
from django.core.servers.basehttp import FileWrapper
from django.db.models import Q
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext
from django.utils import timezone
from easy_pdf.views import PDFTemplateView
from models import *
from forms import *

def home(request):
    current_time = timezone.now()
    alerts = Alert.objects.filter(start_time__lte=current_time,
                                  end_time__gt=current_time)
    news = News.objects.order_by('-date_posted')[:2]
    bills = Legislation.objects.all()[:5]
    news_links = NewsLink.objects.order_by('-date_published')[:5]
    slides = HomepageSlide.objects.filter(active=True)
    calendars = GoogleCalendar.objects.filter(show_on_homepage=True)
    return render(request, 'home.html', locals())

def page(request, page_slug):
    page = get_object_or_404(Page, slug=page_slug)
    return render(request, 'page.html', locals())

def for_students(request):
    users = 'Student'
    desc = "ASG has all the info you need to know about what's happening every week, how to work with a faculty member, how to propose a new project, and more. Our online services help you find a job, sell/buy your books, and get a cab, while our fairs provide opportunities to connect with student groups and find off-campus housing."
    resources = Resource.objects.filter(type='R', users='ST', is_active=True)
    services = Resource.objects.filter(type='S', users='ST', is_active=True)
    return render(request, 'resources.html', locals())

def for_groups(request):
    users = 'Student Group'
    desc = 'Want to know how to start a new student group, finance it, or publicize it? Check out our 2013-14 Student Handbook for all this and more. Also be sure to read the PR Guide for info on how to flyer, reserve rooms and tables, advertise, and print.'
    resources = Resource.objects.filter(type='R', users='SG', is_active=True)
    services = Resource.objects.filter(type='S', users='SG', is_active=True)
    return render(request, 'resources.html', locals())

def calendar(request):
    page_name = 'Calendar'
    calendars = GoogleCalendar.objects.filter(display_on_calendar_page=True)
    return render(request, 'calendar.html', locals())

def office_hours(request):
    page_name = 'Office Hours'
    office_hours = True
    calendars = GoogleCalendar.objects.filter(is_office_hours=True)
    return render(request, 'calendar.html', locals())

news_per_page = 10
def list_news(request):
    all_news = News.objects.order_by('-date_posted')
    p = Paginator(all_news, news_per_page)
    last_page = p.num_pages
    pages = xrange(1, last_page+1)
    page = int(request.GET.get('page', 1))
    news = p.page(page).object_list
    return render(request, 'list_news.html', locals())

legislation_per_page = 10
def list_legislation(request):
    all_legislation = Legislation.objects.order_by('-status_date', '-code')
    p = Paginator(all_legislation, legislation_per_page)
    last_page = p.num_pages
    pages = xrange(1, last_page+1)
    page = int(request.GET.get('page', 1))
    bills = p.page(page).object_list
    return render(request, 'list_legislation.html', locals())

news_links_per_page = 10
def list_news_links(request):
    all_news_links = NewsLink.objects.order_by('-date_published')
    p = Paginator(all_news_links, news_links_per_page)
    last_page = p.num_pages
    pages = xrange(1, last_page+1)
    page = int(request.GET.get('page', 1))
    news_links = p.page(page).object_list
    return render(request, 'list_news_links.html', locals())

def news(request, year, month, slug):
    from_homepage = 'from_homepage' in request.GET
    news = get_object_or_404(News, date_posted__year=year, date_posted__month=month, slug=slug)
    return render(request, 'news.html', locals())

def contact(request):
    exec_board_positions = Position.objects.filter(on_exec_board=True)
    senate_leadership_positions = Position.objects.filter(senate_leadership=True)
    return render(request, 'contact.html', locals())

def cabinet(request):
    exec_members = Person.objects.filter(positions__on_exec_board=True)\
                         .order_by('positions__order')
    return render(request, 'cabinet.html', locals())

def senators(request):
    senators = Person.objects.filter(positions__name='Senator').order_by('groups_represented')
    return render(request, 'senators.html', locals())

def projects(request):
    # iterator() doesn't supply count()
    projects = list(Project.objects.filter(active=True))
    random.shuffle(projects)
    return render(request, 'projects.html', locals())

def committees(request):
    committees = list(Committee.objects.filter(show_in_list=True))
    random.shuffle(committees)
    return render(request, 'committees.html', locals())

def view_project(request, id):
    project = get_object_or_404(Project, id=int(id))
    return render(request, 'view_project.html', locals())

def people(request, id):
    'Display the profile of a single person'
    person = get_object_or_404(Person, id=int(id))
    return render(request, 'person.html', locals())

TUMBLR_API_KEY = os.environ['TUMBLR_API_KEY']
def parse_post_date(post):
    post['date'] = datetime.datetime.strptime(post['date'], '%Y-%m-%d %H:%M:%S GMT')

def blog(request):
    api_url = 'http://api.tumblr.com/v2/blog/nu-asg.tumblr.com/posts/text?api_key=%s' % TUMBLR_API_KEY
    response = requests.get(api_url)
    posts = response.json()['response']['posts']
    map(parse_post_date, posts)
    return render(request, 'blog.html', locals())

def login_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('/edit_profile/')
        auth_form = ASGAuthForm()
    elif request.method == 'POST':
        auth_form = ASGAuthForm(request.POST)
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    person = Person.objects.get(user=user)
                except Person.DoesNotExist:
                    # This is a superuser
                    return redirect('/admin/')
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                login_error = 'Your account has been deactivated'
        else:
            login_error = 'Invalid username or password'
    return render(request, 'login.html', locals())

@login_required
def edit_profile(request):
    'A page for the logged-in user to edit his/her own profile'
    person = get_object_or_404(Person, user=request.user)
    if request.method == 'GET':
        person_form = PersonForm(instance=person)
    elif request.method == 'POST':
        # User submitted the form; update fields
        person_form = PersonForm(request.POST, request.FILES, instance=person)
        if person_form.is_valid():
            # Save the updated data
            person_form.save()
            update_success = True
        person_form = PersonForm(instance=person)
    return render(request, 'edit_profile.html', locals())


# When a visitor selects a senator as "My senator"
def select_senator(request):
    if 'senator_id' in request.GET:
        request.session['my_senator'] = int(request.GET['senator_id'])
    elif 'clear' in request.GET:
        request.session.pop('my_senator', None)
    return redirect('/senators/#table')





# For views limited to ASG exec members
def exec_required(view_fn):
    def _view_fn(*args, **kwargs):
        if args[0].user.groups.filter(name='Exec Board Members').count() > 0:
            return view_fn(*args, **kwargs)
        return redirect('/login/')
    return _view_fn

@exec_required
def exec_tools(request):
    committees = Committee.objects.iterator()
    return render(request, 'exec_tools.html', locals())

@exec_required
def export_roster(request):
    roster = StringIO.StringIO()
    call_command('output_roster', output_dest=roster)
    roster.seek(0) # rewind StringIO to beginning (like a file)
    response = StreamingHttpResponse(FileWrapper(roster), content_type='application/csv')
    response['Content-Disposition'] = 'attachment; filename=asg_roster.csv'
    return response

class ProjectsPDF(PDFTemplateView):
    template_name = 'pdf/projects.html'

    def get_context_data(self, **kwargs):
        return super(ProjectsPDF, self).get_context_data(
            pagesize='letter',
            title='ASG Projects summary',
            projects=Project.objects.filter(active=True).iterator(),
            today=timezone.now(),
            **kwargs
        )

class ResourcesPDF(PDFTemplateView):
    template_name = 'pdf/resources.html'

    def get_context_data(self, **kwargs):
        return super(ResourcesPDF, self).get_context_data(
            pagesize='letter',
            title='ASG Resources summary',
            resources=Resource.objects.filter(is_active=True).iterator(),
            today=timezone.now(),
            **kwargs
        )

