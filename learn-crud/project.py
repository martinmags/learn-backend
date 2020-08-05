from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__, static_folder='static/')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Instantiate and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread':False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Making an API endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
  MenuItems = [i.serialize for i in items]
  return jsonify( MenuItems=MenuItems  )

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJson(restaurant_id, menu_id):
  item = session.query(MenuItem).filter_by(id=menu_id).one()
  serialized = item.serialize
  return jsonify( MenuItem=serialized )

"""
Determines the Route for the function below, HelloWorld()
@app.route('/') calls the @app.route('/hello') which calls HelloWorld()
"""
@app.route('/')
@app.route('/restaurants/')
def restaurantList():
  restaurantList = session.query(Restaurant).all()
  return render_template('restaurants.html', restaurants=restaurantList)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
  return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
  if request.method == 'POST':
    newItem = MenuItem(
      name=request.form['name'], 
      price=request.form['price'],
      description=request.form['description'],
      restaurant_id=restaurant_id
    )
    session.add(newItem)
    session.commit()
    flash("{} has been created!".format(newItem.name))
    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  elif request.method == 'GET':
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('newmenuitem.html', restaurant=restaurant)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
  editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
  if request.method == 'POST':
    originalName = editedItem.name
    originalPrice = editedItem.price
    originalDescription = editedItem.description

    if request.form['name']:
      editedItem.name = request.form['name']
      flash("{} has been updated to {}".format(originalName, editedItem.name))
    if request.form['price']:
      editedItem.price = request.form['price']
      flash("${} has been updated to ${}".format(originalPrice, editedItem.price))
    if request.form['description']:
      editedItem.description = request.form['description']
      flash("{} has been updated to {}".format(originalDescription, editedItem.description))
    session.add(editedItem)
    session.commit()
    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  elif request.method == 'GET':
    return render_template('editmenuitem.html', restaurant_id=restaurant_id, item=editedItem)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
  itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
  if request.method == 'POST':
    deletedName = itemToDelete.name
    session.delete(itemToDelete)
    session.commit()
    flash("%s has been deleted!" % deletedName)
    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  elif request.method == 'GET':
    return render_template('deletemenuitem.html', restaurant_id=restaurant_id, item=itemToDelete)


if __name__ == '__main__':
  # Allows hot reloading
  app.secret_key = 'temp_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port=5000)