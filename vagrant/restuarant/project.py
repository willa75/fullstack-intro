from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items = items)

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