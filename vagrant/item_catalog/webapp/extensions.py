from flask import session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_openid import OpenID
from flask_oauth import OAuth
from flask_principal import Principal, Permission, RoleNeed
from flask_restful import Api

bcrypt = Bcrypt()
oid = OpenID()
oauth = OAuth()

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))

login_manager = LoginManager()

login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(userid):
	from models import User
	return User.query.get(userid)

@oid.after_login
def create_or_login(resp):
	from models import db, User
	username = resp.fullname or resp.fullname or resp.email
	if not username:
		flash('Invalid login. Please try again.', 'danger')
		return redirect(url_for('main.login'))

	user = User.query.filter_by(username=username).first()
	if user is None:
		user = User(username)
		db.session.add(user)
		db.session.commit()

	#redirect to home page
	return redirect(url_for('catalog.home'))

facebook = oauth.remote_app(
	'facebook',
	base_url='https://graph.facebook.com/',
	request_token_url = None,
	access_token_url='/oauth/access_token',
	authorize_url='https://www.facebook.com/dialog/oauth',
	consumer_key='1237978796216280',
	consumer_secret='b76454304072f9eeacb1671157ce72eb',
	request_token_params={'scope':'email'}
)

@facebook.tokengetter
def get_facebook_oauth_token():
	return session.get('facebook_oauth_token')

twitter = oauth.remote_app(
	'twitter',
	base_url='https://api.twitter.com/1.1/',
	request_token_url='https://api.twitter.com/oauth/request_token',
	access_token_url='https://api.twitter.com/oauth/access_token',
	authorize_url='https://api.twitter.com/oauth/authenticate',
	consumer_key='fOe3Zz95dm4C8WJiK2pTSFHqX',
    consumer_secret='EuIV7yAzVMAj9fs5z7T3sa4UqFMWGQvS8rS7v3dDac7nIOEdmP'
)

@twitter.tokengetter
def get_twitter_oauth_token():
	return session.get('twitter_oauth_token')

principals = Principal()
admin_permission = Permission(RoleNeed('admin'))
default_permission = Permission(RoleNeed('default'))
poster_permission = Permission(RoleNeed('poster'))

rest_api = Api()