from flask import Flask, render_template, request, redirect, url_for, flash, 
    jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def restaurantList():
    restaurants = session.query(Restaurant).all()
    return render_template('index.html', restaurants = restaurants)

#An API Endpoint to get a list of restaurants
@app.route('/restaurants/JSON')
def restaurantListJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants =[i.serialize for i in restaurants])

@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newrestaurant = Restaurant(name = request.form['name'])
        session.add(newrestaurant)
        session.commit()
        flash("New restaurant has been added!")
        return redirect(url_for('restaurantList'))
    if request.method == 'GET':
        return render_template('newrestaurant.html')

#Delete restaurant and menu items associated with it
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id)
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("The restaurant has been successfully deleted!")
        return redirect(url_for('restaurantList'))
    if request.method == 'GET':
        return render_template('deleterestaurant.html', restaurant = 
            restaurant)

#Edit name of restaurant
@app.route('restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id)
    if request.method == 'POST':
        if restaurant != []:
            restaurant.name = request.form['name']
            session.add(restaurant)
            session.commit()
            flash("Your message has been edited successfully!")
            return redirect(url_for('restaurantList'))
    if request.method == 'GET':
        return render_template('restaurantedit.html', restaurant = restaurant)

#Display the menu items of a restaurant
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items = items)

#Making an API Endpoint to get list of menu items
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id= 
        restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

#Making an API Endpoint to get one menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantItemJSON(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant_id= 
        restaurant_id, id = menu_id).one()
    return jsonify(MenuItems=item.serialize)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/newitem', methods=[
    'GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newitem = MenuItem(name = request.form['name'], restaurant_id = 
            restaurant_id)
        session.add(newitem)
        session.commit()
        flash("New menu item has been created!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    if request.method == 'GET':
        return render_template('newmenuitem.html', restaurant_id = 
            restaurant_id)
    

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/menuitem/<int:menu_id>/', 
    methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        editItem = session.query(MenuItem).filter_by(id = menu_id, 
            restaurant_id = restaurant_id).one()
        if editItem != []:
            editItem.name = request.form['name']
            session.add(editItem)
            session.commit()
            flash("Your menu item has been edited!")
        return redirect(url_for('restaurantMenu', restaurant_id = 
            restaurant_id))
    elif request.method == 'GET':
        item = session.query(MenuItem).filter_by(id = menu_id,
            restaurant_id = restaurant_id).one()
        return render_template('editmenuitem.html', restaurant_id =
            restaurant_id, menu_id = menu_id, item=item)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>/',
    methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        deleteItem = session.query(MenuItem).filter_by(id = menu_id,
            restaurant_id = restaurant_id).one()
        if deleteItem != []:
            session.delete(deleteItem)
            session.commit()
            flash("Your menu item has been deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id =
            restaurant_id))
    if request.method == 'GET':
        item = session.query(MenuItem).filter_by(id = menu_id,
            restaurant_id = restaurant_id).one()
        return render_template('deletemenuitem.html', restaurant_id =
            restaurant_id, menu_id = menu_id, item = item)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)