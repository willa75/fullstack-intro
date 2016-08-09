from flask import Flask
from utils import get_instance_folder_path
from catalog.main.controllers import main
from catalog.admin.controllers import admin

app = Flask(__name__,
	instance_path = get_instance_folder_path(),
	instance_relative_config = True,
	template_folder='templates')

#enables for loops
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

app.config.from_object('catalog.config.DevelopmentConfig')
app.config.from_pyfile('config.cfg', silent= True)

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')