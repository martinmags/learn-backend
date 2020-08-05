from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Better Design to separate html: 
# Create a class that contains that imports and contains the views

# Create a class that manages database
db = {'user': 'user'}
# Instantiate db session and connect
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
# Memory Storage (Connect to db later)
class webServerHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    try:
      # /
      if self.path.endswith('/'):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += "<h1>Hello "
        output += db['user']
        output += "</h1>"
        output += '''
          <form method='POST' enctype='multipart/form-data' action='/'>
            <h2>What would you like me to say?</h2>
            <input name="message" type="text" >
            <input type="submit" value="Submit">
          </form>'''
        output += "<a href='/restaurants'>View Restaurants List:</a>"
        output += "</body></html>"
        self.wfile.write(output.encode())
        print(output)
        return
      if self.path.endswith('/restaurants'):
        restaurants = session.query(Restaurant).all()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += "<a href='/'>Home</a>"
        output += "<h1>List of all Restaurants</h1>"
        output += "<a href='/restaurants/new'>Add a Restaurant</a>"
        output += "<ul>"
        for restaurant in restaurants:
          output += "<li>"
          output += "<a href='/restaurants/%s/edit'> Rename </a>" % restaurant.id
          output += "<a href='/restaurants/%s/delete'> Delete </a>" % restaurant.id
          output += restaurant.name
          output += "</li>"
        output += "</ul>"
        output += "</body></html>"
        self.wfile.write(output.encode())
        print(output)
        return
      if self.path.endswith('/restaurants/new'):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += "<h1>Add a new Restaurant</h1>"
        output += "<a href='/restaurants'>Back</a>"
        output += '''
          <form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
            <input name='newRestaurantName' type='text' placeholder='Enter the name'>
            <input type='submit' value='Create'>
          </form>'''
        output += "</body></html>"
        self.wfile.write(output.encode())
        print(output)
        return
      if self.path.endswith('/edit'):
        restaurantIDPath = self.path.split("/")[2]
        myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
        if myRestaurantQuery:
          self.send_response(200)
          self.send_header('Content-type', 'text-html')
          self.end_headers()
          output = ""
          output += "<html><body>"
          output += "<h1>%s</h1>" % myRestaurantQuery.name
          output += "<a href='/restaurants'>Back</a>"
          output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
          output += '''
              <input name='newRestaurantName' type='text' placeholder='Enter the name'>
              <input type='submit' value='Rename'>
            </form>
          '''
          output += "</body></html>"
          self.wfile.write(output.encode())
          print(output)
          return
      if self.path.endswith('/delete'):
        restaurantIDPath = self.path.split('/')[2]
        myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
        if myRestaurantQuery:
          self.send_response(200)
          self.send_header('Content-type', 'text-html')
          self.end_headers()
          output = ""
          output += "<html><body>"
          output += "<h1>Are you sure you want to delete %s?</h1>" % myRestaurantQuery.name
          output += "<a href='/restaurants'>Back</a>"
          output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
          output += '''<input type='submit' value='Delete'> </form>'''
          output += "</body></html>"
          self.wfile.write(output.encode())
          print(output)
          return
    except IOError:
      self.send_error(404, 'File Not Found: %s' % self.path)

  def do_POST(self):
    print()
    try:
      if self.path.endswith('/'):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(self.headers.get('Content-length'))
        if ctype == 'multipart/form-data':
          fields = cgi.parse_multipart(self.rfile, pdict)
          messagecontent = fields.get('message')
          db['user'] = "".join(messagecontent[0])
          self.send_response(301)
          self.send_header('content-type', 'text/html')
          self.send_header('Location', '/')
          self.end_headers()
      if self.path.endswith('/restaurants/new'):        
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(self.headers.get('Content-length'))
        if ctype == 'multipart/form-data':
          fields = cgi.parse_multipart(self.rfile, pdict)
          messagecontent = fields.get('newRestaurantName')
          # New Restaurant object
          newRestaurant = Restaurant(name=messagecontent[0])
          session.add(newRestaurant)
          session.commit()
          self.send_response(301)
          self.send_header('content-type', 'text/html')
          self.send_header('Location', '/restaurants')
          self.end_headers()
      if self.path.endswith('/edit'):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(self.headers.get('Content-length'))
        if ctype == 'multipart/form-data':
          fields = cgi.parse_multipart(self.rfile, pdict)
          messagecontent = fields.get('newRestaurantName')
          restaurantIDPath = self.path.split('/')[2]
          myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
          if myRestaurantQuery != []:
            myRestaurantQuery.name = messagecontent[0]
            session.add(myRestaurantQuery)
            session.commit()
            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()
      if self.path.endswith('/delete'):
        restaurantIDPath = self.path.split("/")[2]
        myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
        if myRestaurantQuery:
          session.delete(myRestaurantQuery)
          session.commit()
          self.send_response(301)
          self.send_header('content-type', 'text/html')
          self.send_header('Location', '/restaurants')
          self.end_headers()

    except:
      self.send_error(401, 'Unauthorized action')


def main():
  try:
    server_address = ('', 8080)
    server = HTTPServer(server_address, webServerHandler)
    print("Web Server running on port %s" % server_address[1])
    server.serve_forever()
  except KeyboardInterrupt:
    print(" ^C entered, stopping web server....")
    server.socket.close()

if __name__ == '__main__':
    main()