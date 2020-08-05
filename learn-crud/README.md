# SKILLS LEARNED
================
Managing a database with an ORM (SQLAlchemy)
Creating a webserver
Custom HTTP GET and POST Methods
Using a Flask (Framework) to more efficiently develop


# REQUIRED imports
==================
>>> from sqlalchemy import create_engine
>>> from sqlalchemy.orm import sessionmaker

>>> from database_setup import Base, Restaurant, MenuItem

# INSTANTIATE session; connection to db
=======================================
>>> engine = create_engine('sqlite:///restaurantmenu.db')
>>> Base.metadata.bind = engine
>>> DBSession = sessionmaker(bind = engine)
>>> session = DBSession()

# ADDING an entry to tables
===========================
>>> myFirstRestaurant = Restaurant(name = "Pizza Palace")
>>> session.add(myFirstRestaurant)
>>> session.commit()

# UPDATE an Entry
=================
1. Find entry
>>> entry = session.query( table ).filter_by( property=value ).one()
2. Reset value
>>> entry.property = new_value
3. Add to session
>>> session.add(entry)
4. Commit changes
>>> session.commit()

# DELETE an Entry
=================
1. Find entry
>>> entry = session.query( table ).filter_by( property=value ).one()
2. Delete
>>> session.delete(entry)
3. Commit
>>> session.commit()

# READ/QUERY FROM DB
====================

# SELECT * FROM Restaurant
==========================
>>> session.query(Restaurant).all()
>>> for item in items():
>>>   print(item.id, item.name, item.price, item.restaurant.name)
# SELECT * FROM Restaurant WHERE id=2
=====================================
>>> session.query(Restaurant).filter_by(id=2).one()


# PROTOCOLS: 
============
Grammatical rules that computer follow to communicate with each other

# Transmission Control Protocol (TCP)
=====================================
Break small packets and send from server to clients; 
In the case a packet is failed to deliver, it is re-requested.
# User Datagram Protocol (UDP)
==============================
Good for streaming content like music or video

# Internet Protocol (IP)
========================
Allows data to be properly routed to clients.
# localhost
===========
When server and client have the same IP address.

# Hyper Text Transfer Protocol (HTTP)
=====================================
Clients tell servers what they want through HTTP methods
such as a GET or POST request. In response to a request,
the server returns to the Client a status code and/or 
any requested resources like an html, css, js file.
# Basic Status Codes
====================
200: Successful GET
301: Successful POST
404: File not found

# How to improve dev experience
===============================
Instead of using raw [sql], use an [orm]
Instead of creating custom [http_methods], use a [backend_framework] (django, flask)

# FLASK
=======
Connecting database
Using Templates to separate HTML and Python
url_for to manage routes
Forms to capture data from users
message flashing to notify users successful changes to db
Using JSON
# URLS
======
"path/<type: variable_name>/path"
url_for(
   method_name_to_execute, 
   values_to_pass_to_method's_parameters
)
render_template( 
  html_filename, 
  values_to_pass_to_template_html 
)
# Sessions
==========
Provide a more personal experience by storing user data
# FLASH
=======
Display a successful message to notify users the changes to the db
flash("insert message here")
get_flashed_messages()
1. Add flash("message") after a session.commit() in project.py
2. In the respective view, add the following:
  {%  with messages=get_flashed_messages() %}
    {% if messages %}
      {% for message in messages %}
      <ul>
        <li>{{message}}</li>
      </ul>
      {% endfor %}
    {% endif %}
  {% endswith %}
# STATIC FILES
==============
http://exploreflask.com/en/latest/static.html
1. create a directory 'static' (store css, media, etc.)
2. add tag into respective html file
<link rel=stylesheet type=text/css href="{{ url_for('static', filename='styles.css')}}">
NOTE: static files are cached in the browser; to update cache on reload, do CTRL+SHIFT+R

# ITERATIVE DEVELOPMENT PROCESS
===============================
[ ] Mock-ups(Design db, pages, mvp use cases, urls )
[ ] Routing(Navigate to all urls correctly)
[ ] Templates and Forms (HTML)
[ ] CRUD Functionality
[ ] API Endpoints: create a serialize function in db classes.

  [ ] 1. You can fetch this data by using the fetch or axios api in JAVASCRIPT
      fetch(url of api endpoint).then((response) =>{
        // JSON data will arrive here as a part of response
        return response.json();
      }).then((data)=>{
        // Dynamically display 'data' on a div tag in HTML
      }).catch((error)=>{
        // error handling
      })
  [ ] 2. Display on HTML dynamically when fetch finishes collecting the JSON data
      <div id=myData> Then target this id in Javascript with... 
      let mainContainer = document.getElementById("myData")
      Then dynamically generate html in javascript to display the data from fetch

[ ] Styling & Message Flashing

# OTHER CONSIDERATIONS BEFORE DEPLOYMENT
========================================
Security: https://pythonhosted.org/Flask-Security/

# DEPLOYMENT
============
https://flask.palletsprojects.com/en/1.1.x/deploying/