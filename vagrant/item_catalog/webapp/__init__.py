from config import DevConfig
from flask import Flask
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed

from models import db
from controllers.catalog import catalog_blueprint
from controllers.main import main_blueprint
from .extensions import bcrypt, oid,login_manager, principals, rest_api
from .controllers.rest.auth import AuthApi
from .controllers.rest.item import ItemApi
def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    #initialize db and extensions
    db.init_app(app)
    bcrypt.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    rest_api.add_resource(
    	ItemApi, 
    	'/api/post',
    	'/api/post/<int:item_id>',
    	endpoint='api'
    )
    rest_api.add_resource(
    	AuthApi, 
    	'/api/auth'
    )
    rest_api.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    #initialize app controllers
    app.register_blueprint(main_blueprint)
    app.register_blueprint(catalog_blueprint)
    
    return app