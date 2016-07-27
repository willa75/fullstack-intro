from flask import Flask
from catalog.main.controllers import main
from catalog.admin.controllers import admin

app = Flask(__name__)

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(admin, url_prefix='/admin')