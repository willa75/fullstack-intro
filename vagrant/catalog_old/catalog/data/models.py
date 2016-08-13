from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
	__tablename__ = 'item'
	name = db.Column(db.String(100), nullable = False)
	id = db.Column(db.Integer, primary_key = True)
	description = db.Column(db.String(250))