from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

CLIENT_ID = json.loads(
  open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def restaurantList():
    restaurants = session.query(Restaurant).all()
    return render_template('index.html', restaurants = restaurants)

@app.route('/gconnect', methods=['POST'])
def gconnect():
  if request.args.get('state') != login_session['state']:
    response = make_response(json.dumps('Invalid state parameter'), 401)
    response.headers['Content-Type'] =  'application/json'
    return response
  code = request.data
  try:
    #Upgrade authorization code to credentials object
    oauth_flow = flow_from_clientsecrets('client_secrets.json',
      scope='')
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code) 
  except FlowExchangeError:
    response = make_response(json.dumps('Failed to upgrade the authorization code'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  #Make sure token is valid
  access_token = credentials.access_token
  url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
  h = httplib2.Http()
  result = json.loads(h.request(url, 'GET')[1])
  #If there was an error in the access token info, abort
  if result.get('error') is not None:
    response = make_response(json.dumps(result.get('error')), 50)
    response.headers['Content-Type'] = 'application/json'
  #Verify that the access token is used for the intended user
  gplus_id = credentials.id_token['sub']
  if result['user_id'] != gplus_id:
    response = make_response(json.dumps("Token's user ID doesn't match given user ID"), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  #Verify that the access token is valid for this app
  if result['issued_to'] != CLIENT_ID:
    response = make_response(json.dumps("Token's client ID does not match app's."), 401)
    print "Token's client ID does not match app's."
    response.headers['Content-Type'] = 'application/json'
    return response
  #Check to see if user is already logged in
  stored_credentials = login_session.get('credentials')
  stored_gplus_id = login_session.get('gplus_id')
  if stored_credentials is not None and gplus_id == stored_gplus_id:
    response = make_response(json.dumps('Current user is already connected.'), 200)
    response.headers['Content-Type'] = 'application/json'

  #Store the access token in the session for later use.
  login_session['credentials'] = credentials
  login_session['gplus_id'] = gplus_id

  #Get user info
  userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
  params = {'access_token': credentials.access_token, 'alt':'json'}
  answer = requests.get(userinfo_url, params = params)
  data = json.loads(answer.text)

  login_session['provider'] = 'google'
  login_session['username'] = data["name"]
  login_session['picture'] = data["picture"]
  login_session['email'] = data["email"]

  #Check to see if user already registered
  user_id = getUserID(login_session['email'])
  if not user_id:
    user_id = createUser(login_session)
  login_session['user_id'] = user_id

  output= ''
  output += '<h1> Welcome, '
  output += login_session['username']

  output += '!</h1>'
  output += '<img src="'
  output += login_session['picture']
  output += ' " style="width: 300px; height: 300px;border-radius: 150px; -webkit-border-radius: 150px;-moz-border-radius: 150px;">'
  flash("you are now logged in as %s" %login_session['username'], 'success')
  return output


@app.route("/fbconnect", methods=['POST'])
def fbconnect():
  if request.args.get('state') != login_session['state']:
    response = make_response(json.dumps('Invalid state parameter.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  access_token = request.data

  #Exchange client token for long-lived server-side token with GET /oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-lived-token}
  app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
  app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
  url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
  h = httplib2.Http()
  result = h.request(url, 'GET')[1]
  #Use token to get user info from API
  userinfo_url = 'https://graph.facebook.com/v2.5/me'
  #strip expire tag from access token
  token = result.split("&")[0]
  token = token.split("=")[1]

  url = 'https://graph.facebook.com/v2.5/me?fields=id,name,email&access_token=%s' % token
  h = httplib2.Http()
  result = h.request(url, 'GET')[1]
  data = json.loads(result)

  login_session['provider'] = 'facebook'
  login_session['username'] = data['name']
  login_session['email'] = data['email']
  login_session['facebook_id'] = data['id']

  #Get user picture
  url = 'https://graph.facebook.com/v2.5/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
  print url
  h = httplib2.Http()
  result = h.request(url, 'GET')[1]
  data = json.loads(result)
  
  print data
  login_session['picture'] = data["data"]["url"]

  #see if user exists
  user_id = getUserID(login_session['email'])
  if not user_id:
    user_id = createUser(login_session)
  login_session['user_id'] = user_id

  output= ''
  output += '<h1> Welcome, '
  output += login_session['username']

  output += '!</h1>'
  output += '<img src="'
  output += login_session['picture']
  output += ' " style="width: 300px; height: 300px;border-radius: 150px; -webkit-border-radius: 150px;-moz-border-radius: 150px;">'
  flash("you are now logged in as %s" %login_session['username'], 'success')
  return output

@app.route("/disconnect")
def disconnect():
  if 'provider' in login_session:
    if login_session['provider'] == 'google':
      gdisconnect()
      del login_session['gplus_id']
      del login_session['credentials']
    if login_session['provider'] == 'facebook':
      fbdisconnect()
      del login_session['facebook_id']

    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    flash("You have been successfully logged out.", 'success')
    return redirect(url_for('showRestaurants'))
  else:
    flash("You were never logged in to begin with!")
    return redirect(url_for('showRestaurants'))
  

@app.route("/fbdisconnect")
def fbdisconnect():
  facebook_id = login_session['facebook_id']
  url = 'https://graph.facebook.com/%s/permissions' % facebook_id
  h = httplib2.Http()
  result = h.request(url, 'DELETE')[1]


@app.route("/gdisconnect")
def gdisconnect():
  #Only disconnect connected users.
  credentials = login_session.get('credentials')
  if credentials is None:
    response = make_response(json.dumps('Current user not connected'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  #Revoke current token
  access_token = credentials.access_token
  url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
  h = httplib2.Http()
  result = h.request(url, 'GET')[0]
  json.dumps(result)
  if result['status'] == '200':
    response = make_response(json.dumps('Successfully disconnected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
  else:
    #Send Error message because of invalid token
    response = make_response(json.dumps(result), 400)
    response.headers['Content-Type'] = 'application/json'
    return response

def createUser(login_session):
  newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
  session.add(newUser)
  session.commit()
  user = session.query(User).filter_by(email = login_session['email']).one()
  return user.id

def getUserInfo(user_id):
  user = session.query(User).filter_by(id = user_id).one()
  return user

def getUserID(email):
  try:
    user = session.query(User).filter_by(email = email).one()
    return user.id
  except:
    return None

#An API Endpoint to get a list of restaurants
@app.route('/restaurants/JSON')
def restaurantListJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants =[i.serialize for i in restaurants])

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
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
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