# Create a Virtualenv
virtualenv venv
# Activate virtualenv
source venv/bin/activate


# Install Django
pip install Django


# Create a project
django-admin startproject mysite


# Project Files
mysite/:      container for the project (can be renamed)
./manage.py:  cmdline utility; allows interaction w/ django
./mysite/:    python package for the project; need its name

./mysite/__init__.py: lets python know this is a python package
./mysite/settings.py: configs for django project
./mysite/urls.py:     url declaractions; a "table of contents"
./mysite/asgi.py:     entry-point for ASGI-compatible web servers
./mysite/wsgi.py:     entry-point for WSGI-compatible web servers


# Run django server (OPTIONAL: port 8080)
cd mysite
python manage.py runserver 8080
# Note:
Don't use this server for production, only for development.


# Projects vs apps
App:      specific web app, a smaller piece of a bigger project
Project:  container for config and app(s)
A project can have multiple apps; an app can be in multiple projects
# Note:
We are creating the polls app in the same dir level as the manage.py,
so we can import it as its own top-level module.


# Create an app (called polls)
python manage.py startapp polls


# App Files
./migrations/
./templates/:  describes how django will load and render view templates
./__init__.py: python package
./admin.py:    register apps available for admin
./apps.py:
./models.py:   database table schema 
./tests.py:
./views.py:    input webrequest; output webresponse; frontend interface
./urls.py:     manages urls and function call in views


# Database Setup (DEFAULT: sqlite3)
# TODO: Learn to setup PostGresql 
# Timezone 
https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

# Default installed apps for the common case
django.contrib.admin:         admin site
django.contrib.auth:          authentication system
django.contrib.contenttypes:  framework for content types
django.contrib.sessions:      session framework
django.contrib.messages:      messaging framework
django.contrib.staticfiles:   framework for managing static files

# Creates necessary tables in the database for the 'installed apps'
python manage.py migrate

# If created a new app... (OPTIONAL: polls)
python manage.py makemigrations polls
# ^ Creates an editable file polls/migrations/0001_initial.py
# Run migrate again to apply the migration to the db
python manage.py migrate



# Playing with API in Python shell
python manage.py shell
# Import recently created models
>>> from polls.models import Choice, Question
# Query all questions in db
>>> Question.objects.all()
# Create a new Question
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
# Save object into DB
>>> q.save()
# Access model fields
>>> q.id
>>> q.question_text
>>> q.pub_date
# Create three choices under a specific question object as a set
>>> q.choice_set.create(choice_text='Not much', votes=0)
>>> q.choice_set.create(choice_text='The sky', votes=0)
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)
>>> c.question
# Output choice set for question q.
>>> q.choice_set.all()
# Delete a choice c
>>> c.delete()


# Creating Admin user
python manage.py createsuperuser
username: Admin
email: admin@example.com
password: testing1234
# Now you can login at "/admin" url
# Register Question objects in admin interface in 'polls/admin.py'
from .models import Question
admin.site.register(Question)


# URL Routing explained
Let's say the url is "/polls/34/".
Django will run the mysite.urls module, find 'urlpatterns', and
traverse the patterns in order. It strips off the matching text
"polls/", then sends the remaining "34/" to the matching string
in the paths. It then calls the detail method specified in the 
path, and continues to run the detail method in views.py and 
returns the respective view.
# detail(request=<HttpRequest object>, question_id=34)


# A bit more about Views
Views return either an HttpResponse object or Http404.
A few example use cases:
  Read records from a database
  Generate a PDF file
  Output XML
  Create a ZIP file
  ...
# Request object
request.POST: a dictionary-like object that allows accessing of
submitted data by keyname. EX: request.POST['choice'] returns id 
of the selected choice as a string.
# KeyError
KeyError if request.POST['choice'] was not provided in POST data.
Code section redisplays the question form with an error msg if
choice isn't given.
# POST data Web dev tip:
Always return an HttpResponseRedirect after successfully dealing with
POST data to prevent data from double posting if user hits the back
button.
# Django's Generic Views System (less code)
Listview and DetailView both use a default template; they are called 
  <app name>/<model name>_list.html 
  <app name>/<model name>_default.html 
respectively.
We use template_name to tell ListView to use our existing
  "polls/index.html" template
1. Convert the URLconf.
2. Delete some of the old, unneeded views.
3. Introduce new views based on Django's generic views.



# Templating
Instead of directly hard coding the page design in the view, use 
django's template system.
# Create a directory called templates in polls
# Create a polls directory in templates
# Create an index.html file in polls 
# "polls/templates/polls/index.html"
# Use the render shortcut in Views.py
render(request, 'polls/index.html', context)
# Use the get_object_or_404() shortcut for error handling
question = get_object_or_404(Question, pk=question_id)
return render(request, 'polls/details.html', {'question':question})

# Django looks up the URL definition specified in polls.urls 'name'
path('<int:question_id>/', views.detail, name='detail')
# Removing hardcoded urls in templates by using the {% url %} tag
Change href="/polls/{{ question.id }}/" to 
       href="{% url 'detail' question.id %}"
# Add namespacing to URL names to prevent name conflicts between apps
app_name = 'polls'
# In templates/polls/index.html
Change href="{% url 'detail' question.id %}" to 
       href="{% url 'polls:detail' question.id %}"

# HTML: Write a minimal form
Must use {% csrf_token % } in <form> to help protect against 
Cross Site Request Forgeries


# LOCKING and Race Conditions
Optimistic Concurrency Control (OCC) aka Optimistic Locking: 
Locking incurs overhead only if there's a conflict; best if
app mostly does not have conflicting transactions.
  0. add a timestamp or versionnumber column to the table.
  1. read a record
  2. compare the record with last timestamped update.
    a. if record hasn't changed, write back/save to db
    b. if record has changed, abort transaction and re-start it.

Pessimistic Concurrency Control (PCC) aka Pessismistic Locking:
Reduced overhead on conflict.
1. Lock record for exclusive use until finished.


# TESTING
# Run polls test file
python manage.py test polls
# Run test client to simulate user interacting with the code at view lvl
python manage.py shell
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()
# NOTE: DB is reset on every test method
# Apply assertion checks with response object
>>> from django.urls import reverse
>>> response = self.client.get(reverse('polls:index'))
>>> response.status_code
>>> response.content

# Styling
Create the following directory route 'polls/static/polls'
# Note: The inner 'polls' is for namespacing to prevent conflicts
Create 'polls/static/polls/style.css'
Link the stylesheet in the 'polls/templates/polls/index.html':
  {% load static %}
  <link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}">  
DON'T forget to restart server to see the changes.


# Admin
If you want to override templates,
use django.contrib.admin.AdminSite.site_header attribute.


# Packaging your app
https://docs.djangoproject.com/en/3.0/intro/reusable-apps/


# QUESTIONS
Shouldn't the vote method be under the detailview class in views.py?
If given a one to many relation like the example in the tutorial,
  how can I filter the query such that I only get the Questions with
  choices?